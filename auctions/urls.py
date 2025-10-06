from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.New_listing, name="new_listing"),
    path("listing_details/<int:listing_id>/", views.Listing_details, name="listing_details")
]
