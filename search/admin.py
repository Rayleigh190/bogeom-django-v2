from django.contrib import admin

# Register your models here.
from .models import Market, MarketItems, Item


class MarketItemsModelAdmin(admin.ModelAdmin):
  readonly_fields = ('updated_at',)
  list_display = ['market_id', 'item_id', 'item_price', 'updated_at']
  list_display_links = ['market_id', 'item_id', 'item_price', 'updated_at']


class ItemModelAdmin(admin.ModelAdmin):
  list_display = ['item_name', 'item_search_count']
  list_display_links = ['item_name', 'item_search_count']


class MarketModelAdmin(admin.ModelAdmin):
  list_display = ['market_name', 'road_address']
  list_display_links = ['market_name', 'road_address']


admin.site.register(Item, ItemModelAdmin)
admin.site.register(Market, MarketModelAdmin)
admin.site.register(MarketItems, MarketItemsModelAdmin)