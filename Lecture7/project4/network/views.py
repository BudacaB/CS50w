from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .models import Post, Profile, User


def index(request):
    if request.method == "POST":
        post_body = request.POST["post"]
        post = Post(user = request.user, post = post_body)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/index.html")


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

@login_required(login_url=reverse_lazy("login"))
def profile(request, username):
    following = None
    user = User.objects.get(username = username)
    request_user = request.user == user
    user_posts = Post.objects.all().filter(user = user).order_by("-created").all()
    if request.method == "POST":
        if request.POST['action'] == 'Follow':
            profile = Profile(user = request.user, following = user)
            profile.save()
            return render(request, "network/profile.html", {
                "username": user.username,
                "request_user": request_user,
                "user_posts": user_posts,
                "following": True
            })
        elif request.POST['action'] == 'Unfollow':
            pass
    else:
        if ((not request_user and not Profile.objects.filter(user = request.user)) or
        (not request_user and request.user.profile not in user.followers.all())):
            following = False
        else:
            following = True
        return render(request, "network/profile.html", {
            "username": user.username,
            "request_user": request_user,
            "user_posts": user_posts,
            "following": following
        })