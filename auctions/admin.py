from django.contrib import admin
from .models import User, Listing

class ListingtAdmin(admin.ModelAdmin):
	list_display = ("date", "user", "title", "price", "category")
# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingtAdmin)
