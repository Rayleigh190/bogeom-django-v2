from rest_framework import serializers
from search.models import Market, MarketItems, Item


class MarketCreateSerializer(serializers.ModelSerializer):
  
  class Meta:
    model =  Market
    fields = [
      'market_name',
      'latitude',
      'longitude',
      'road_address',
    ]


class ItemCreateSerializer(serializers.ModelSerializer):

  class Meta:
    model = Item
    fields = [
      'item_name',
      'item_search_count',
    ]


class MarketItemsCreateSerializer(serializers.ModelSerializer):

  class Meta:
    model = MarketItems
    fields = [
      'market_id',
      'item_id',
      'item_price',
    ]