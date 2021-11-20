from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse

from .models import Post, User


def index(request):
    if request.method == "POST":
        post_body = request.POST["post"]
        post = Post(user = request.user, post = post_body)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")
        # posts = Post.objects.all()
        # posts = Post.objects.all().order_by("-created").all()
        # return JsonResponse([post.serialize() for post in posts], safe=False)
        # return render(request, "network/index.html", {
        #     "posts": posts
        # })


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def all_posts(request):
    posts = Post.objects.all().order_by("-created").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

def profile(request):
    return render(request, "network/profile.html")