from django import urls
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        url = request.POST["url"]
        category = request.POST["category"]
        listing = Listing(title=title, description=description, starting_bid=starting_bid, url=url, category=category, listed_by=request.user)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html")

def view_listing(request, listing_id):
    bids_count = Bid.objects.filter(listing = listing_id).count()
    listing = Listing.objects.get(pk=listing_id)
    watchlisted = Watchlist.objects.filter(listing_id = listing_id, user_id = request.user.id)
    if request.method == "GET":  
        if not watchlisted:     
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids_count": bids_count
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "watchlisted": watchlisted,
                "bids_count": bids_count
            })
    elif request.method == "POST":
        bid = request.POST.get('bid', 0)
        if bid != 0:
            if bids_count == 0:
                new_bid = Bid(listing=listing, bidder=request.user, bid=bid)
                # TODO - save bid and move to other cases
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "bids_count": bids_count
            })
        else:
            if not watchlisted:
                watchlist = Watchlist(user=request.user, listing=listing)
                watchlist.save()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "watchlisted": True,
                    "bids_count": bids_count
                })
            else:
                watchlisted[0].delete()
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "bids_count": bids_count
                })


