from django.contrib import admin
from .models import *

class auction(admin.ModelAdmin):
    list_display = ("title", "user", "creation_date", "active")

class bds(admin.ModelAdmin):
    list_display = ("user", "listingid", "bid")

class comme(admin.ModelAdmin):
    list_display = ("user", "listingid", "comment")

class watchl(admin.ModelAdmin):
    list_display = ("watch_list", "user")

# Register your models here.
admin.site.register(Listing, auction)
admin.site.register(Bid, bds)
admin.site.register(Comment, comme)
admin.site.register(Watchlist, watchl)