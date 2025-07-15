from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid
from .forms import CreateListingForm, MakeBid

@login_required
def create_listing_view(request: HttpResponse):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            imageURL = form.cleaned_data["imageURL"]
            initBid = form.cleaned_data["initBid"]
            category = form.cleaned_data["category"]
            user = request.user

            listing = Listing(
                title = title,
                description = description,
                imageURL = imageURL,
                initBid = initBid,
                createUser = user
            )
            if category:
                listing.category.set([category])
            listing.save()
            return render(request, "auctions/index.html")
    return render(request, "auctions/create_listing.html",
                  context={
        "create_listing" : CreateListingForm
        })

def listing_view(request : HttpResponse, pk ):
    listing = Listing.objects.all()[pk - 1]
    biger_bid = Bid.objects.filter(listing = listing).order_by('-value').first()
    if biger_bid:
        biger_bid_value = biger_bid.value
    else:
        biger_bid_value = listing.initBid
    if request.method =="POST":
        form  = MakeBid(request.POST,listing=listing)
        if form.is_valid():
            value = form.cleaned_data[value]
            user = request.user
            bid = Bid(
                value = value,
                user = user,
                listing = listing
            )
            bid.save()
            return render(request, "auctions/index.html")

    elif request.method == "GET":
        if request.user:
            makeBid = MakeBid(listing=listing)
        else:
            makeBid = ""
        return render(
            request, "auctions/listing.html",
            context={
                "listing" : listing,
                "make_bid" : makeBid,
                "pk" : pk,
                "biger_bid" : biger_bid_value
            }
        )


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", context={
        "listings" : listings
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
