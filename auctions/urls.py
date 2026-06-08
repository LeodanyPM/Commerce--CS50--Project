from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name= "watchlist"),
    path("my_listings", views.my_listings, name= "my_listings"),
    path("categories", views.categories, name= "categories"),
    path("categories/<str:category>", views.categories_listing, name= "categories_listing"),
    path('listing/<int:listing_id>/watchlist/', views.toggle_watchlist, name='toggle_watchlist'),
    path("listing/<int:id>", views.listing, name= "listing"),
    path('listing/<int:listing_id>/bid/', views.place_bid, name='place_bid'),
    path('listing/<int:listing_id>/close/', views.close_auction, name='close_auction'),
]

