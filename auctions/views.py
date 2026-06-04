from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .forms import ListingForm, CommentForm
from django.contrib import messages
from .util import optimize_image
from .models import User, Listing, Watchlist, Comment, Bid, Category 
from decimal import Decimal, InvalidOperation
 

def index(request):
    my_data = Listing.objects.filter(active=True)
    context = {'listing' : my_data }    
    return render(request, "auctions/index.html", context)


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
            messages.success(request, "Artículo guardado correctamente.")
            return HttpResponseRedirect(reverse("index"))   
    else:
        form = ListingForm()  # GET: formulario vacío
    return render(request, 'auctions/create_listing.html', {'form': form})
    
"""def listing(request, id):
   
    ad = get_object_or_404(Listing, id=id)
    
    
    comments = ad.comments.all()
    
    if request.method == 'POST':
        
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para comentar.")
            return redirect('listing_detail', id=id)
            
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.listing = ad
            comment.save()
            
            messages.success(request, "Comentario publicado.")
            return redirect('listing', id=id)  
    else:
        form = CommentForm()

    return render(request, 'auctions/listing.html', {
        'ad': ad,
        'comments': comments,
        'form': form
    })"""
    
def listing(request, id):
    # ✅ Obtiene el anuncio o 404
    ad = get_object_or_404(Listing, id=id)
    
    # ✅ Comentarios ordenados por fecha (gracias a Meta.ordering en Comment)
    comments = ad.comments.all()
    
    # ✅ Puja más alta (gracias a Meta.ordering = ['-amount'] en Bid)
    current_bid = ad.bids.first()
    
    # ✅ Estado de watchlist y ganador (solo si está autenticado)
    is_in_watchlist = False
    is_winner = False
    
    if request.user.is_authenticated:
        # Usa related_name='watchlist_items' definido en Watchlist.listing
        is_in_watchlist = ad.watched_by.filter(user=request.user).exists()
        
        # Verifica si ganó (subasta cerrada + winner == usuario)
        if not ad.active and ad.winner == request.user:
            is_winner = True

    # ✅ Manejo del formulario de comentarios
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
def watchlist(request):	
	# Obtener directamente los Listings que el usuario sigue
        # Ajusta 'watchlist_items' al related_name que definiste en tu modelo
        listings = Listing.objects.filter(watched_by__user=request.user).select_related('user')  # Opcional: si necesitas datos del creador
        context = {'listing':listings}
        return render(request, 'auctions/watchlist.html', context) 
        

@login_required(login_url='/login') 
def my_listings(request):
    my_listings= Listing.objects.filter(user=request.user)
    context = {'listing':my_listings}
    return render(request, 'auctions/my_listings.html',context)

@login_required(login_url='/login')
def toggle_watchlist(request, listing_id):
    """Añade o elimina el anuncio de la watchlist del usuario"""
    listing = get_object_or_404(Listing, id=listing_id)
    
    # get_or_create devuelve (objeto, created: bool)
    watch_entry, created = Watchlist.objects.get_or_create(
        user=request.user, 
        listing=listing
    )
    
    if not created:
        watch_entry.delete()
        messages.info(request, "Eliminado de tu lista de seguimiento.")
    else:
        messages.success(request, "Añadido a tu lista de seguimiento.")
        
    return redirect('listing', id=listing_id)
    
@login_required
def place_bid(request, listing_id):
    """Registra una puja validando monto mínimo y superioridad"""
    listing = get_object_or_404(Listing, id=listing_id)
    
    if not listing.active:
        messages.error(request, "Esta subasta ya está cerrada.")
        return redirect('listing', id=listing_id)

    if request.method == 'POST':
        amount_str = request.POST.get('bid_amount', '').strip()
        try:
            amount = Decimal(amount_str)
        except (InvalidOperation, ValueError):
            messages.error(request, f"Ingresa un monto válido.")
            return redirect('listing', id=listing_id)

        highest_bid = listing.bids.first()
        
        #  Validación según requisitos CS50
        if not highest_bid:
            if amount < listing.price:
                messages.error(request, f"La puja debe ser al menos igual al precio inicial (${listing.price}).")
                return redirect('listing', id=listing_id)
        else:
            if amount <= highest_bid.amount:
                messages.error(request, f"La puja debe ser superior a la actual (${highest_bid.amount}).")
                return redirect('listing', id=listing_id)

        # ✅ Guarda la puja
        Bid.objects.create(listing=listing, user=request.user, amount=amount)
        messages.success(request, f"¡Puja de ${amount} registrada exitosamente!")

    return redirect('listing', id=listing_id)
    
@login_required
def close_auction(request, listing_id):
    """Cierra la subasta y asigna al mejor postor como ganador"""
    listing = get_object_or_404(Listing, id=listing_id)
    
    # Solo el creador puede cerrar
    if listing.user != request.user:
        messages.error(request, "Solo el creador del anuncio puede cerrar esta subasta.")
        return redirect('listing', id=listing_id)
        
    if not listing.active:
        messages.warning(request, "La subasta ya está cerrada.")
        return redirect('listing', id=listing_id)

    highest_bid = listing.bids.first()
    if highest_bid:
        listing.winner = highest_bid.user
        messages.success(request, f"Subasta cerrada. Ganador: {highest_bid.user.username} (${highest_bid.amount}).")
    else:
        messages.info(request, "Subasta cerrada sin ofertas.")
        
    listing.active = False
    listing.save()
    return redirect('listing', id=listing_id)
    
def categories(request):
    categories= Category.objects.all()
    context = {'categories':categories}
    return render(request,  "auctions/categories.html", context)
    
def categories_listing(request, category):
        listings = Listing.objects.filter(category__category=category)  # Opcional: si necesitas datos del creador
        context = {'listing':listings}
        return render(request, 'auctions/watchlist.html', context)
