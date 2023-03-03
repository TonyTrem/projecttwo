from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import datetime

from .models import User, Listing, Bid, Comment, Watchlist

class CommentForm(forms.Form):
    comment = forms.CharField(label="Comment", max_length=64)

class BidForm(forms.Form):
    bid = forms.IntegerField(label="Bid")

class ListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Description", max_length=64)
    starting_bid = forms.IntegerField(label="Starting Bid")
    image_url = forms.CharField(label="Image URL", max_length=64)
    category = forms.CharField(label="Category", max_length=64)

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
    
def listing(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            listing = Listing.objects.get(pk=listing_id)
            if bid > listing.current_bid:
                listing.current_bid = bid
                listing.bid_count += 1
                listing.save()
                user = User.objects.get(pk=request.user.id)
                bid = Bid(user=user, listing=listing, bid=bid)
                bid.save()
                return HttpResponseRedirect(reverse("listing", args=[listing_id]))
            else:
                return render(request, "auctions/listing.html", {
                    "listing": Listing.objects.get(pk=listing_id),
                    "message": "Bid must be higher than current bid."
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk=listing_id),
                "form": form
            })
    else:
        return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id)
    })

def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            user = User.objects.get(pk=request.user.id)
            listing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, user=user, creation_date=datetime.now(), active=True)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })
    else:
        return render(request, "auctions/create.html", {
            "form": ListingForm()
        })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listing.objects.values_list('category', flat=True).distinct()
    })

def category(request, category):
    return render(request, "auctions/category.html", {
        "listings": Listing.objects.filter(category=category)
    })

def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    return render(request, "auctions/watchlist.html", {
        "listings": Watchlist.objects.filter(user=user)
    })

def add_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=request.user.id)
    watchlist = Watchlist(user=user, listing=listing)
    watchlist.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    user = User.objects.get(pk=request.user.id)
    watchlist = Watchlist.objects.get(user=user, listing=listing)
    watchlist.delete()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def comment(request, listing_id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["comment"]
            listing = Listing.objects.get(pk=listing_id)
            user = User.objects.get(pk=request.user.id)
            comment = Comment(user=user, listing=listing, comment=comment)
            comment.save()
            return HttpResponseRedirect(reverse("listing", args=[listing_id]))
        else:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk=listing_id),
                "form": form
            })
    else:
        return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id)
    })

def close(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    listing.active = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=[listing_id]))

def closed(request):
    return render(request, "auctions/closed.html", {
        "listings": Listing.objects.filter(active=False)
    })

def winner(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    winner = Bid.objects.filter(listing=listing).order_by('-bid').first()
    return render(request, "auctions/winner.html", {
        "listing": listing,
        "winner": winner
    })

def my_listings(request):
    return render(request, "auctions/my_listings.html", {
        "listings": Listing.objects.filter(user=request.user.id)
    })

def my_bids(request):
    return render(request, "auctions/my_bids.html", {
        "listings": Listing.objects.filter(bid__user=request.user.id)
    })

def my_comments(request):
    return render(request, "auctions/my_comments.html", {
        "comments": Comment.objects.filter(user=request.user.id)
    })