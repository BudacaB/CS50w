from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import Bill, Food, Fun, Transport, User

@csrf_exempt
def index(request):
    if request.method == "POST":
        data = json.loads(request.body)
        expense_date = data.get("date")
        expense = data.get("expense")
        if data.get("type") == "food":   
            expense = Food(user = request.user, amount = expense, created = expense_date)
            expense.save()
            return HttpResponse(status=201)
        elif data.get("type") == "bills":
            expense = Bill(user = request.user, amount = expense, created = expense_date)
            expense.save()
            return HttpResponse(status=201)
        elif data.get("type") == "transport":
            expense = Transport(user = request.user, amount = expense, created = expense_date)
            expense.save()
            return HttpResponse(status=201)
        elif data.get("type") == "fun":
            expense = Fun(user = request.user, amount = expense, created = expense_date)
            expense.save()
            return HttpResponse(status=201)
    else:
        return render(request, "budget/index.html")


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


@csrf_exempt
@login_required(login_url=reverse_lazy("login"))
def edit(request, expenseType):
    if request.method == "PUT":
        updated_amount = json.loads(request.body).get("amount")
        if expenseType == "Food":
            expense = Food.objects.get(pk=request.GET.get('id'), user = request.user)
            expense.amount = updated_amount
            expense.save()
            updatedExpense = Food.objects.get(pk=request.GET.get('id'), user = request.user)
        elif expenseType == "Bills":
            expense = Bill.objects.get(pk=request.GET.get('id'), user = request.user)
            expense.amount = updated_amount
            expense.save()
            updatedExpense = Bill.objects.get(pk=request.GET.get('id'), user = request.user)
        elif expenseType == "Transport":
            expense = Transport.objects.get(pk=request.GET.get('id'), user = request.user)
            expense.amount = updated_amount
            expense.save()
            updatedExpense = Transport.objects.get(pk=request.GET.get('id'), user = request.user)
        elif expenseType == "Fun":
            expense = Fun.objects.get(pk=request.GET.get('id'), user = request.user)
            expense.amount = updated_amount
            expense.save()
            updatedExpense = Fun.objects.get(pk=request.GET.get('id'), user = request.user)
        return JsonResponse({
            "updatedExpense": updatedExpense.amount
        }, status=200)
    elif request.method == "DELETE":
        if expenseType == "Food":
            Food.objects.filter(pk=request.GET.get('id'), user = request.user).delete()
        elif expenseType == "Bills":
            Bill.objects.filter(pk=request.GET.get('id'), user = request.user).delete()
        elif expenseType == "Transport":
            Transport.objects.filter(pk=request.GET.get('id'), user = request.user).delete()
        elif expenseType == "Fun":
            Fun.objects.filter(pk=request.GET.get('id'), user = request.user).delete()
        return HttpResponse(status=204)
    else:
        if expenseType == "food":
            expenses = Food.objects.filter(created = request.GET.get('date'), user = request.user)
        elif expenseType == "bills":
            expenses = Bill.objects.filter(created = request.GET.get('date'), user = request.user)
        elif expenseType == "transport":
            expenses = Transport.objects.filter(created = request.GET.get('date'), user = request.user)
        elif expenseType == "fun":
            expenses = Fun.objects.filter(created = request.GET.get('date'), user = request.user)
        return render(request, "budget/edit.html", {
            "expense_name": expenseType.title(),
            "expenses": expenses,
            "date": request.GET.get('date')
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


def get_stats(request, date):
    if request.user.is_authenticated:
        food_expenses = Food.objects.filter(created = date, user = request.user)
        bills_expenses = Bill.objects.filter(created = date, user = request.user)
        transport_expenses = Transport.objects.filter(created = date, user = request.user)
        fun_expenses = Fun.objects.filter(created = date, user = request.user)
        food = get_expense_total(food_expenses)
        bills = get_expense_total(bills_expenses)
        transport = get_expense_total(transport_expenses)
        fun = get_expense_total(fun_expenses)
        total = food + bills + transport + fun
        food_total_percentage = get_percentage(total, food)
        bills_total_percentage = get_percentage(total, bills)
        transport_total_percentage = get_percentage(total, transport)
        fun_total_percentage = get_percentage(total, fun)
        return JsonResponse({
            "food_stats": food_total_percentage,
            "bills_stats": bills_total_percentage,
            "transport_stats": transport_total_percentage,
            "fun_stats": fun_total_percentage,
            "food": food,
            "bills": bills,
            "transport": transport,
            "fun": fun
        }, status=200)
    else:
        return JsonResponse({
            "food": 0,
            "bills": 0,
            "transport": 0,
            "fun": 0
        }, status=200)


@csrf_exempt
@login_required(login_url=reverse_lazy("login"))
def profile(request):
    if request.method == "DELETE":
        user = User.objects.filter(pk=request.user.id).delete()
        logout(request)
        return HttpResponseRedirect(reverse("index"))
    else:
        user = User.objects.get(pk=request.user.id)
        return render(request, "budget/profile.html", {
            "date_joined": user.date_joined
        })


@csrf_exempt
@login_required(login_url=reverse_lazy("login"))
def get_range_stats(request):
    food_expenses = Food.objects.filter(created__range=[request.GET.get('start'), request.GET.get('end')], user = request.user)
    bills_expenses = Bill.objects.filter(created__range=[request.GET.get('start'), request.GET.get('end')], user = request.user)
    transport_expenses = Transport.objects.filter(created__range=[request.GET.get('start'), request.GET.get('end')], user = request.user)
    fun_expenses = Fun.objects.filter(created__range=[request.GET.get('start'), request.GET.get('end')], user = request.user)
    food = get_expense_total(food_expenses)
    bills = get_expense_total(bills_expenses)
    transport = get_expense_total(transport_expenses)
    fun = get_expense_total(fun_expenses)
    total = food + bills + transport + fun
    food_total_percentage = get_percentage(total, food)
    bills_total_percentage = get_percentage(total, bills)
    transport_total_percentage = get_percentage(total, transport)
    fun_total_percentage = get_percentage(total, fun)
    return JsonResponse({
            "food_stats": food_total_percentage,
            "bills_stats": bills_total_percentage,
            "transport_stats": transport_total_percentage,
            "fun_stats": fun_total_percentage,
            "food": food,
            "bills": bills,
            "transport": transport,
            "fun": fun
    }, status=200)