from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.New_listing, name="new_listing"),
    path("listing_details/<int:listing_id>/", views.Listing_details, name="listing_details"),
    path('listing/<int:listing_id>/bid/', views.Place_bid, name='place_bid'),
    path('listing/<int:listing_id>/watchlist/', views.Toggle_watchlist, name='toggle_watchlist'),
    path('listing/<int:listing_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path("watchlist/", views.watchlist, name="watchlist")
]
