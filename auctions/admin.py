from django.contrib import admin
from .models import User, Listing, Watchlist

class ListingtAdmin(admin.ModelAdmin):
	list_display = ("date", "user", "title", "price", "category")

class WatchlistAdmin(admin.ModelAdmin):
	list_display = ("user","listing")
# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingtAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
