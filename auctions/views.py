from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

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
    return render(request, "auctions/newlisting.html", {
        "form": NewPageform()
    })


class NewPageform(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control w-75 mb-2'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control w-75 mb-2', 'rows': 3}), label="Description",)
    start_bid = forms.DecimalField(label="Start bid",max_digits=10,decimal_places=2,min_value=0.01,widget=forms.NumberInput(attrs={'class': 'form-control w-75 mb-2', 'step': '0.01'}))
    image_url = forms.URLField(label="Image URL", widget=forms.URLInput(attrs={'class': 'form-control w-75 mb-2'}))
    category = forms.ModelChoiceField(label="category", queryset=Category.objects.all(),  widget=forms.Select(attrs={'class': 'form-control w-75 mb-2'}))
    