from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from datetime import datetime

from .models import User, Listing, Bid

class BidForm(forms.Form):
    bid = forms.DecimalField(label="Bid", max_digits=10, decimal_places=2)

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
            listing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, user=user, current_bid=starting_bid, active=True, creation_date=datetime.now)
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
    
def createbid(request, listing_id):
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.cleaned_data["bid"]
            user = User.objects.get(pk=request.user.id)
            listing = Listing.objects.get(pk=listing_id)
            if bid > listing.current_bid:
                listing.current_bid = bid
                listing.save()
                bid = Bid(user=user, listing=listing, bid=bid)
                bid.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
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
            "listing": Listing.objects.get(pk=listing_id),
            "form": BidForm()
        })