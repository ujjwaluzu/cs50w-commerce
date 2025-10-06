from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import User, Category, Comment, Listing, Bid


def index(request):
    return render(request, "auctions/index.html", {
        "listing": Listing.objects.filter(active=True)
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

def New_listing(request):
    if request.method == "POST":
        form = NewPageform(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.author = request.user
            listing.save()
            return redirect('listing_details', listing_id=listing.id)
    else:
        form = NewPageform()
    return render(request, "auctions/newlisting.html", {
        "form": form
    })


class NewPageform(forms.ModelForm):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control w-75 mb-2'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-75 mb-2', 'rows': 3}), label="Description",)
    start_bid = forms.DecimalField(label="Start bid",max_digits=10,decimal_places=2,min_value=0.01,widget=forms.NumberInput(attrs={'class': 'form-control w-75 mb-2', 'step': '0.01'}))
    image = forms.URLField(label="Image URL", widget=forms.URLInput(attrs={'class': 'form-control w-75 mb-2'}))
    category = forms.ModelChoiceField(label="category", queryset=Category.objects.all(),  widget=forms.Select(attrs={'class': 'form-control w-75 mb-2'}))
    
    class Meta:
        model = Listing
        fields = ['title', 'description', 'start_bid', 'image', 'category']


def Listing_details(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    is_owner = request.user == listing.author

    highest_bid_message = None
    highest_bid = listing.bids.order_by('-amount').first()  # Get current highest bid

    if highest_bid and request.user.is_authenticated:
        # Only show highest bidder message if auction is still active
        if highest_bid.user == request.user and listing.active:
            highest_bid_message = f"You are currently the highest bidder with ₹{highest_bid.amount}!"

    # Determine auction winner for closed auctions
    highest_bidder = highest_bid.user if highest_bid else None
    highest_bid_amount = highest_bid.amount if highest_bid else None

    context = {
        "listing": listing,
        "owner": is_owner,
        "highest_bid_message": highest_bid_message,
        "highest_bidder": highest_bidder,
        "highest_bid_amount": highest_bid_amount
    }

    return render(request, "auctions/listing_details.html", context)



def Place_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    highest_bid_message = None

    if request.method == "POST" and request.user.is_authenticated:
        try:
            bid_amount = float(request.POST.get('bid_amount'))
        except (TypeError, ValueError):
            highest_bid_message = "Invalid bid amount."
        else:
            current_price = listing.current_price()
            if bid_amount <= current_price:
                highest_bid_message = f"Your bid must be higher than the current price (${current_price})."
            else:
                # Save the bid
                Bid.objects.create(item=listing, user=request.user, amount=bid_amount)
                highest_bid_message = f"You are now the highest bidder with ${bid_amount}!"

    # Render the listing details template directly
    return render(request, "auctions/listing_details.html", {
        "listing": listing,
        "highest_bid_message": highest_bid_message
    })
def Toggle_watchlist(request, listing_id):
        if not request.user.is_authenticated:
            return redirect('login')

        listing = get_object_or_404(Listing, pk=listing_id)

        if request.user in listing.watchlisted_by.all():
            listing.watchlisted_by.remove(request.user)
        else:
            listing.watchlisted_by.add(request.user)

        return redirect('listing_details', listing_id=listing_id)

def add_comment(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.method == "POST" and request.user.is_authenticated:
        comment_text = request.POST.get('comment')
        if comment_text:
            Comment.objects.create(item=listing, user=request.user, comment=comment_text)
    return redirect('listing_details', listing_id=listing_id)

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    listing_id = comment.item.id
    if request.user == comment.user:
        comment.delete()
    return redirect('listing_details', listing_id=listing_id)

def watchlist(request):
    if not request.user.is_authenticated:
        return redirect('login')

    watchlisted_items = request.user.watchlist.all()  # because related_name="watchlist"

    return render(request, "auctions/watchlist.html", {
        "listing": watchlisted_items
    })


def close_bid(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    if request.user == listing.author:
        listing.active = False
        listing.save()
    return redirect('listing_details', listing_id=listing.id)

def CategoryShow(request):
    return render(request, "auctions/category.html", {
        "category": Category.objects.all()
    })

def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category, active=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })