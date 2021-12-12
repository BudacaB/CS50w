from datetime import time
from typing import Match
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Bill, Food, Fun, Transport, User

def index(request):
    if request.method == "POST":
        if 'food_expense' in request.POST:      
            expense_date = request.POST["food_date"]
            expense_body = request.POST["food_expense"]
            expense = Food(user = request.user, amount = expense_body, created = expense_date)
            expense.save()
            return HttpResponseRedirect(reverse("index"))
        elif 'bills_expense' in request.POST:
            expense_date = request.POST["bill_date"]
            expense_body = request.POST["bills_expense"]
            expense = Bill(user = request.user, amount = expense_body, created = expense_date)
            expense.save()
            return HttpResponseRedirect(reverse("index"))
        elif 'transport_expense' in request.POST:
            expense_date = request.POST["transport_date"]
            expense_body = request.POST["transport_expense"]
            expense = Transport(user = request.user, amount = expense_body, created = expense_date)
            expense.save()
            return HttpResponseRedirect(reverse("index"))
        elif 'fun_expense' in request.POST:
            expense_date = request.POST["fun_date"]
            expense_body = request.POST["fun_expense"]
            expense = Fun(user = request.user, amount = expense_body, created = expense_date)
            expense.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_anonymous:
            return render(request, "budget/index.html")
        else: 
            food_expenses_today = Food.objects.filter(created = now().date(), user = request.user)
            bills_expenses_today = Bill.objects.filter(created = now().date(), user = request.user)
            transport_expenses_today = Transport.objects.filter(created = now().date(), user = request.user)
            fun_expenses_today = Fun.objects.filter(created = now().date(), user = request.user)
            food = get_expense_total(food_expenses_today)
            bills = get_expense_total(bills_expenses_today)
            transport = get_expense_total(transport_expenses_today)
            fun = get_expense_total(fun_expenses_today)
            total = food + bills + transport + fun
            food_total_percentage = get_percentage(total, food)
            bills_total_percentage = get_percentage(total, bills)
            transport_total_percentage = get_percentage(total, transport)
            fun_total_percentage = get_percentage(total, fun)
            return render(request, "budget/index.html", {
                "food": food_total_percentage,
                "bills": bills_total_percentage,
                "transport": transport_total_percentage,
                "fun": fun_total_percentage
            })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "budget/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "budget/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "budget/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "budget/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "budget/register.html")

@login_required(login_url=reverse_lazy("login"))
def edit(request, expense):
    if expense == "food":
        expenses = Food.objects.filter(created = now().date(), user = request.user)
    elif expense == "bills":
        expenses = Bill.objects.filter(created = now().date(), user = request.user)
    elif expense == "transport":
        expenses = Transport.objects.filter(created = now().date(), user = request.user)
    elif expense == "fun":
        expenses = Fun.objects.filter(created = now().date(), user = request.user)
    return render(request, "budget/edit.html", {
        "expense_name": expense.title(),
        "expenses": expenses
    })

def get_expense_total(expenses):
    total = 0
    for expense in expenses:
        total = total + expense.amount
    return total

def get_percentage(total, expense):
    if total is not 0:
        return "{:.2f}".format(expense / total * 100)
    else:
        return 0