from django import urls
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.exclude(active=False)
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
    listing = Listing.objects.get(pk=listing_id)
    listed_by_current_user = listing.listed_by == request.user
    watchlisted = Watchlist.objects.filter(listing_id = listing_id, user_id = request.user.id)
    if request.method == "GET":
        return view_listing_get(request, listing, listing_id, watchlisted, listed_by_current_user)
    elif request.method == "POST":
        return view_listing_post(request, listing, listing_id, watchlisted, listed_by_current_user)

def view_listing_get(request, listing, listing_id, watchlisted, listed_by):
    bids_count = Bid.objects.filter(listing = listing_id).count()
    try:
        current_bid = Bid.objects.filter(listing = listing_id).latest('created')
        if current_bid.bidder == request.user:  
            if listing.active:
                if watchlisted:   
                    return render_template(request, listing, watchlisted, bids_count, "Your bid is the current bid", None, None)
                else:
                    return render_template(request, listing, None, bids_count, "Your bid is the current bid", None, None)
            else:
                if watchlisted:   
                    return render_template(request, listing, watchlisted, bids_count, "Your won the bid!", None, None)
                else:
                    return render_template(request, listing, None, bids_count, "Your won the bid!", None, None)
        else:
            if watchlisted:    
                return render_template(request, listing, watchlisted, bids_count, "", None, listed_by) 
            else:
                return render_template(request, listing, None, bids_count, "", None, listed_by)
    except Bid.DoesNotExist:
        if not watchlisted:    
            return render_template(request, listing, None, bids_count, "", None, listed_by) 
        else:
            return render_template(request, listing, watchlisted, bids_count, "", None, listed_by)

def view_listing_post(request, listing, listing_id, watchlisted, listed_by):
    bids_count = Bid.objects.filter(listing = listing_id).count()
    try:
        current_bid = Bid.objects.filter(listing = listing_id).latest('created')
        if request.POST['action'] == 'Watchlist':
            return add_to_watchlist(request, listing, bids_count, current_bid, listed_by)
        elif request.POST['action'] == 'Remove from Watchlist':
            return remove_from_watchlist(request, listing, watchlisted, bids_count, current_bid, listed_by)
        elif request.POST['action'] == 'Close':
            return close(request, listing, watchlisted, bids_count, listed_by)
        elif request.POST['action'] == 'Place Bid':
            return bidding(request, listing, listing_id, watchlisted, current_bid, bids_count, listed_by)
        elif request.POST['action'] == 'Post Comment':
            return comment(request, listing, listing_id, watchlisted, listed_by)
    except Bid.DoesNotExist:
        dummy_user = User()
        current_bid = Bid(listing=listing, bidder=dummy_user, bid=0)
        if request.POST['action'] == 'Watchlist':
            return add_to_watchlist(request, listing, bids_count, current_bid, listed_by)
        elif request.POST['action'] == 'Remove from Watchlist':
            return remove_from_watchlist(request, listing, watchlisted, bids_count, current_bid, listed_by)
        elif request.POST['action'] == 'Close':
            return close(request, listing, watchlisted, bids_count, listed_by)
        elif request.POST['action'] == 'Place Bid':
            return bidding(request, listing, listing_id, watchlisted, current_bid, bids_count, listed_by)
        elif request.POST['action'] == 'Post Comment':
            return comment(request, listing, listing_id, watchlisted, listed_by)

def add_to_watchlist(request, listing, bids_count, current_bid, listed_by):
    watchlist_create = Watchlist(user=request.user, listing=listing)
    watchlist_create.save()
    if current_bid.bidder == request.user:
        return render_template(request, listing, True, bids_count, "Your bid is the current bid", None, None)
    else:
        return render_template(request, listing, True, bids_count, "", None, listed_by)

def remove_from_watchlist(request, listing, watchlisted, bids_count, current_bid, listed_by):
    watchlisted[0].delete()
    if current_bid.bidder == request.user:
        return render_template(request, listing, None, bids_count, "Your bid is the current bid", None, None)
    else:
        return render_template(request, listing, None, bids_count, "", None, listed_by)

def bidding(request, listing, listing_id, watchlisted, current_bid, bids_count, listed_by):
    bid = request.POST.get('bid')
    if float(bid) >= listing.starting_bid and float(bid) > current_bid.bid:
        new_bid = Bid(listing=listing, bidder=request.user, bid=bid)
        new_bid.save()
        Listing.objects.filter(pk=listing_id).update(starting_bid = float(bid))
        listing = Listing.objects.get(pk=listing_id)
        bids_count = Bid.objects.filter(listing = listing_id).count()
        current_bid = Bid.objects.filter(listing = listing_id).latest('created')
        if current_bid.bidder == request.user:
            if watchlisted:
                return render_template(request, listing, watchlisted, bids_count, "Your bid is the current bid", None, None)
            else:
                return render_template(request, listing, None, bids_count, "Your bid is the current bid", None, None)
        if watchlisted:
            return render_template(request, listing, watchlisted, bids_count, "", None, listed_by)
        else:
            return render_template(request, listing, None, bids_count, "", None, listed_by)
    elif float(bid) < listing.starting_bid or float(bid) <= current_bid.bid:
        if watchlisted:
            return render_template(request, listing, watchlisted, bids_count, "", "The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any).", None)
        else:
            return render_template(request, listing, None, bids_count, "", "The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any).", None)


def close(request, listing, watchlisted, bids_count, listed_by):
    listing.active = False
    listing.save()
    if watchlisted:
        return render_template(request, listing, watchlisted, bids_count, "", None, listed_by)
    else:
        return render_template(request, listing, None, bids_count, "", None, listed_by)

def comment(request, listing, listing_id, watchlisted, listed_by):
    comment = request.POST.get('comment')
    new_comment = Comment(comment=comment, user=request.user, listing=listing)
    new_comment.save()
    return view_listing_get(request, listing, listing_id, watchlisted, listed_by)

def render_template(request, listing, watchlisted, bids_count, current_bid, message, listed_by):
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlisted": watchlisted,
        "bids_count": bids_count,
        "current_bid": current_bid,
        "message": message,
        "listed_by": listed_by,
        "comments": Comment.objects.filter(listing = listing).order_by('-created')
    })

def watchlist(request):
    print(request.user.watching)
    watchlisted = set()
    for watchlisted_listing in request.user.watching.all():
        for listing in Listing.objects.filter(id = watchlisted_listing.listing_id):
            watchlisted.add(listing)
    return render(request, "auctions/watchlist.html", {
        "watchlisted": watchlisted
    })

def categories(request):
    return render(request, "auctions/categories.html")