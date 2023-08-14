from django.contrib import admin

# Register your models here.
from .models import Market, MarketItems, Item

admin.site.register(Market)
admin.site.register(MarketItems)
admin.site.register(Item)