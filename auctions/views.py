from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from decimal import Decimal, InvalidOperation
from .forms import ListingForm, CommentForm
from .util import optimize_image
from .models import User, Listing, Watchlist, Comment, Bid, Category 


 

def index(request):
    my_data = Listing.objects.filter(active=True).annotate(max_bid=Max('bids__amount')).order_by('-date')
    context = {'listing' : my_data }    
    return render(request, "auctions/index.html", context)

@login_required(login_url='/login') 
def watchlist(request):	
    listings = Listing.objects.filter(watched_by__user=request.user).select_related('user')
    context = {'listing':listings}
    return render(request, 'auctions/watchlist.html', context) 
        

@login_required(login_url='/login') 
def my_listings(request):
    my_listings= Listing.objects.filter(user=request.user)
    context = {'listing':my_listings}
    return render(request, 'auctions/my_listings.html',context)
    
def categories(request):
    categories= Category.objects.all()
    context = {'categories':categories}
    return render(request,  "auctions/categories.html", context)


def categories_listing(request, category):
        listings = Listing.objects.filter(category__category=category)
        context = {'listing':listings, 'category':category}
        return render(request, 'auctions/categories_listing.html', context)

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

@login_required(login_url='/login')     
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES) 
        if form.is_valid():
            
            listing = form.save(commit=False)
            listing.user = request.user
            listing.save()
            messages.success(request, "Article saved correctly.")
            return HttpResponseRedirect(reverse("index"))   
    else:
        form = ListingForm() 
    return render(request, 'auctions/create_listing.html', {'form': form})
    
    
def listing(request, id):
    ad = get_object_or_404(Listing, id=id)
    comments = ad.comments.all()
    current_bid = ad.bids.first()
    is_in_watchlist = False
    is_winner = False
    
    # watchlist and winner checking
    if request.user.is_authenticated:
        is_in_watchlist = ad.watched_by.filter(user=request.user).exists()
        if not ad.active and ad.winner == request.user:
            is_winner = True

    # form comments
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.listing = ad 
            comment.save()
            return redirect('listing', id=id)
    else:
        form = CommentForm()

    return render(request, 'auctions/listing.html', {
        'ad': ad,
        'comments': comments,
        'form': form,
        'current_bid': current_bid,
        'is_in_watchlist': is_in_watchlist,
        'is_winner': is_winner,
    })

    


@login_required(login_url='/login')
def toggle_watchlist(request, listing_id):
    """Add or remove the ad from the user's watchlist"""
    listing =get_object_or_404(Listing, id=listing_id)
    watch_entry, created = Watchlist.objects.get_or_create(
        user=request.user, 
        listing=listing
    )
    
    if not created:
        watch_entry.delete()
        messages.info(request, "Removed from your watchlist.")
    else:
        messages.success(request, "Added to your watchlist.")
        
    return redirect('listing', id=listing_id)
    
@login_required
def place_bid(request, listing_id):
    """Register a bid, validating the minimum and maximum amount."""
    listing= get_object_or_404(Listing, id=listing_id)
    
    if not listing.active:
        messages.error(request, "This auction is now closed.")
        return redirect('listing', id=listing_id)

    if request.method == 'POST':
        amount_str = request.POST.get('bid_amount', '').strip()
        try:
            amount = Decimal(amount_str)
        except (InvalidOperation, ValueError):
            messages.error(request, f"Enter a valid amount.")
            return redirect('listing', id=listing_id)

        highest_bid = listing.bids.first()
                
        if not highest_bid:
            if amount < listing.price:
                messages.error(request, f"The bid must be at least equal to the starting price (${listing.price}).")
                return redirect('listing', id=listing_id)
        else:
            if amount <= highest_bid.amount:
                messages.error(request, f"The bid must be higher than the current one (${highest_bid.amount}).")
                return redirect('listing', id=listing_id)

        
        Bid.objects.create(listing=listing, user=request.user, amount=amount)
        messages.success(request, f"Bid of ${amount} successfully registered!")

    return redirect('listing', id=listing_id)
    
@login_required
def close_auction(request, listing_id):
    """Close the auction and award the highest bidder the prize."""
    listing = get_object_or_404(Listing, id=listing_id)
        
    if listing.user != request.user:
        messages.error(request, "Only the creator of the ad can close this auction.")
        return redirect('listing', id=listing_id)
        
    if not listing.active:
        messages.warning(request, "The auction is now closed.")
        return redirect('listing', id=listing_id)

    highest_bid = listing.bids.first()
    if highest_bid:
        listing.winner = highest_bid.user
        messages.success(request, f"Auction closed. Winner: {highest_bid.user.username} (${highest_bid.amount}).")
    else:
        messages.info(request, "Auction closed with no bids.")
        
    listing.active = False
    listing.save()
    return redirect('listing', id=listing_id)
    

