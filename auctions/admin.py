from django.contrib import admin
from .models import User, Listing, Watchlist, Comment, Category, Bid

class ListingtAdmin(admin.ModelAdmin):
	list_display = ("date", "user", "title", "price", "category")

class WatchlistAdmin(admin.ModelAdmin):
	list_display = ("user","listing")
	
class CommenttAdmin(admin.ModelAdmin):
      list_display = ("listing", "user")	
# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingtAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Comment, CommenttAdmin)
admin.site.register(Category)
admin.site.register(Bid)
