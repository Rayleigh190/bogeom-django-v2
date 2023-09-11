from django.db import models

# Create your models here.

class Item(models.Model):
  id = models.AutoField(
    primary_key=True
  )
  item_name = models.CharField(
    max_length=100
  )
  item_img  = models.ImageField(
    null=True,
    blank=True
  )
  item_search_count = models.PositiveIntegerField(
    default = 0
  )

  def __str__(self):
    return self.item_name


class Market(models.Model):
  id = models.AutoField(
    primary_key=True
  )
  market_name = models.CharField(
    max_length = 128
  )
  latitude = models.FloatField()
  longitude = models.FloatField()
  road_address = models.TextField()

  def __str__(self):
    return self.market_name


class MarketItems(models.Model):
  id = models.AutoField(
    primary_key=True
  )
  market_id = models.ForeignKey(
    Market,
    on_delete=models.CASCADE
  )
  item_id = models.ForeignKey(
    Item,
    on_delete=models.CASCADE
  )
  item_price = models.PositiveIntegerField(
    default = 0
  )
  updated_at = models.DateTimeField(# 옮기기
    auto_now = True
  )