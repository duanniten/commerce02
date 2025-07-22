from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from decimal import Decimal

from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment
from .forms import CreateListingForm, MakeBid, CommentForm
from .utils import getCurrentBidValue, getComments

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

@login_required
def watchlist(request: HttpResponse):
    listings = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", context={
        "listings" : listings
    })

@login_required
def makebid(request : HttpResponse):
    msg = None
    if request.method == "POST":
        pk = int(request.POST.get("pk"))
        listing = Listing.objects.all()[pk - 1]
        currentBidValue, currentBid = getCurrentBidValue(listing)
        if Decimal(request.POST.get("value")) > currentBidValue:
            if listing.closed == False:
                bid = Bid(
                    value = Decimal(request.POST.get("value")),
                    user = request.user,
                    listing = listing
                )
                bid.save()
            else:
                msg = "This listing is closed"
        else:
            msg = "Bid should be bigger than current bid"
    return listing_view(request, pk= pk, msg= msg)

@login_required
def changeWatchList(request:HttpResponse):
    if request.method == "POST":
        pk = int(request.POST.get("pk"))
        listing = Listing.objects.all()[pk-1]

        if listing in request.user.watchlist.all():
            request.user.watchlist.remove(listing)
        else:
            request.user.watchlist.add(listing)
    return listing_view(request, pk, msg = None)

@login_required
def makeComment(request:HttpResponse):
    if request.method == "POST":
        pk = int(request.POST.get("pk"))
        listing = Listing.objects.all()[pk-1]
        user = request.user

        comment = Comment(
            comment = request.POST.get("comment"),
            listing = listing,
            user = user
        )
        comment.save()
    return listing_view(request, pk, msg=None)

@login_required
def closeListing(request:HttpResponse):
    msg = None
    if request.method == "POST":
        pk = int(request.POST.get("pk"))
        listing = Listing.objects.all()[pk-1]
        if request.user == listing.createUser:
            listing.closed = True
            listing.save()
        else:
            msg = "User should be the creat user to close"
    return listing_view(request, pk, msg)

def listing_view(request : HttpResponse, pk , msg = None):
    listing = Listing.objects.all()[pk-1]
    currentBidValue, currentBid = getCurrentBidValue(listing)
    comments = getComments(listing)
    closedText = ""
    if listing.closed == True:
            makeBid = ""
            closeListing = ""
            watchlist = ""
            closedText = ""
            if currentBid == None:
                closedText  = "Closed with no bids"
            elif request.user == currentBid.user:
                closedText  = "you won this bid" 

    elif request.user.is_authenticated:
            closedText= ""
            if request.user == listing.createUser:
                makeBid = ""
                closeListing = True
            else: 
                makeBid = MakeBid(listing=listing)
                closeListing = False
            
            if listing in request.user.watchlist.all():
                watchlist = "Remove from"
            else:
                watchlist = "Add to"
        
    else:
        makeBid = ""
        closeListing = ""
        watchlist = ""
        closedText = ""
    return render(
        request, "auctions/listing.html",
        context={
            "listing" : listing,
            "make_bid" : makeBid,
            "pk" : pk,
            "biger_bid" : currentBidValue,
            "closeListing" : closeListing,
            "watchlist" : watchlist,
            "message" : msg,
            "closedText": closedText,
            "comments": comments,
            "makecomment": CommentForm
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
