from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from operator import attrgetter
from django.core.paginator import Paginator
import json

from django.views.decorators.csrf import csrf_exempt

from .models import Likes, Post, Profile, User


def index(request):
    if request.method == "POST":
        post_body = request.POST["post"]
        post = Post(user = request.user, post = post_body)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        posts = Post.objects.all().order_by("-created").all()
        user_liked_posts = Likes.objects.filter(liked_by = request.user)
        user_liked_posts_unpacked = set()
        for post in user_liked_posts:
            user_liked_posts_unpacked.add(post.post)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": page_obj,
            "user_liked_posts": user_liked_posts_unpacked
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

@login_required(login_url=reverse_lazy("login"))
def profile(request, username):
    following = None
    user = User.objects.get(username = username)
    followers_count = user.followers.count()
    following_count = user.following.count() 
    request_user = request.user == user
    user_posts = Post.objects.all().filter(user = user).order_by("-created").all()
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        if request.POST['action'] == 'Follow':
            profile = Profile(follower = request.user, following = user)
            profile.save()
            followers_count = user.followers.count()
            following = True
        elif request.POST['action'] == 'Unfollow':
            Profile.objects.filter(follower = request.user, following = user).delete()
            followers_count = user.followers.count()
            following = False
        return render(request, "network/profile.html", {
            "username": user.username,
            "followers_count": followers_count,
            "following_count": following_count,
            "request_user": request_user,
            "user_posts": page_obj,
            "following": following
        })
    else:
        if (not request_user and not Profile.objects.filter(follower = request.user, following = user)):
            following = False
        else:
            following = True
        return render(request, "network/profile.html", {
            "username": user.username,
            "followers_count": followers_count,
            "following_count": following_count,
            "request_user": request_user,
            "user_posts": page_obj,
            "following": following
        })

def following(request):
    posts = list()
    following = request.user.following.all()
    for followed_user in following:
        print(followed_user.following)
        for post in Post.objects.all().filter(user = followed_user.following).order_by("-created").all():
            posts.append(post)
    posts.sort(key = attrgetter('created'), reverse = True)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "posts": page_obj
    })

@csrf_exempt
def update_post(request, postId):
    post = Post.objects.get(pk=postId)
    data = json.loads(request.body)
    updatedPost = data.get("post")
    post.post = updatedPost
    post.save()
    updatedPost = Post.objects.get(pk=postId)
    print(post.post)
    return JsonResponse({
        "updatedPost": updatedPost.post
    }, status=200)

@csrf_exempt
def like_post(request, postId, username):
    user = User.objects.get(username = username)
    post = Post.objects.get(pk=postId)
    if (post.likes.count() == 0 or not Likes.objects.filter(post = post, liked_by = user)):
        like = Likes(post = post, liked_by = user)
        like.save()
        return HttpResponse(status=200)
    else:
        like = Likes.objects.filter(post = post, liked_by = user).delete()
        return HttpResponse(status=200)