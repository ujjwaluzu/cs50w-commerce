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
        "listing": Listing.objects.all()
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
            return redirect('index')
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
    return render(request, "auctions/listing_details.html", {
        "owner": is_owner,
        "listing": listing
    })