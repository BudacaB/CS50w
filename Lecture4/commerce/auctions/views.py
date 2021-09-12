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

# this method either gets a listing, either it posts for watchlist or a bid
def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listed_by_current_user = listing.listed_by == request.user
    watchlisted = Watchlist.objects.filter(listing_id = listing_id, user_id = request.user.id)
    if request.method == "GET":
        return view_listing_get(request, listing, listing_id, watchlisted, listed_by_current_user)
    elif request.method == "POST":
        return view_listing_post(request, listing, listing_id, watchlisted)

# TODO continue new logic for closing
def view_listing_get(request, listing, listing_id, watchlisted, listed_by):
    bids_count = Bid.objects.filter(listing = listing_id).count()
    try:
        current_bid = Bid.objects.filter(listing = listing_id).latest('created')
        if current_bid.bidder == request.user:  
            if not watchlisted:   
                return render_template(request, listing, None, bids_count, "Your bid is the current bid", None, listed_by)
            else:
                return render_template(request, listing, watchlisted, bids_count, "Your bid is the current bid", None, listed_by)
        else:
            if not watchlisted:    
                return render_template(request, listing, None, bids_count, "", None, listed_by) 
            else:
                return render_template(request, listing, watchlisted, bids_count, "", None, listed_by)
    except Bid.DoesNotExist:
        if not watchlisted:    
            return render_template(request, listing, None, bids_count, "", None, listed_by) 
        else:
            return render_template(request, listing, watchlisted, bids_count, "", None, listed_by)

def view_listing_post(request, listing, listing_id, watchlisted):
    bid = request.POST.get('bid', 0)
    current_bid = Bid.objects.filter(listing = listing_id).latest('created')
    bids_count = Bid.objects.filter(listing = listing_id).count()
    if float(bid) != 0:
        return bidding(request, bid, listing, listing_id, current_bid, bids_count)
    else:
        return watchlist(request, listing, watchlisted, bids_count, current_bid)

def bidding(request, bid, listing, listing_id, current_bid, bids_count):
    if float(bid) >= listing.starting_bid and float(bid) > current_bid.bid:
        new_bid = Bid(listing=listing, bidder=request.user, bid=bid)
        new_bid.save()
        Listing.objects.filter(pk=listing_id).update(starting_bid = float(bid))
        listing = Listing.objects.get(pk=listing_id)
        bids_count = Bid.objects.filter(listing = listing_id).count()
        current_bid = Bid.objects.filter(listing = listing_id).latest('created')
        if current_bid.bidder == request.user:
            return render_template(request, listing, None, bids_count, "Your bid is the current bid", None)
        return render_template(request, listing, None, bids_count, "", None)
    elif float(bid) < listing.starting_bid or float(bid) <= current_bid.bid:
        return render_template(request, listing, None, bids_count, "", "The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any).")

def watchlist(request, listing, watchlisted, bids_count, current_bid):
    if current_bid.bidder == request.user:
        if not watchlisted:
            watchlist = Watchlist(user=request.user, listing=listing)
            watchlist.save()
            return render_template(request, listing, True, bids_count, "Your bid is the current bid", None)
        else:
            watchlisted[0].delete()
            return render_template(request, listing, None, bids_count, "Your bid is the current bid", None)
    else:
        if not watchlisted:
            watchlist = Watchlist(user=request.user, listing=listing)
            watchlist.save()
            return render_template(request, listing, True, bids_count, "", None)
        else:
            watchlisted[0].delete()
            return render_template(request, listing, None, bids_count, "", None)
                
def render_template(request, listing, watchlisted, bids_count, current_bid, message, listed_by):
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlisted": watchlisted,
        "bids_count": bids_count,
        "current_bid": current_bid,
        "message": message,
        "listed_by": listed_by
    })