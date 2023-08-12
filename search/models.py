from django.db import models

# Create your models here.

class Item(models.Model):
  item_name = models.CharField(
    max_length=100
  )
  item_img  = models.ImageField(
    null=True
  )
  item_search_count = models.PositiveIntegerField(
    default = 0
  )

  def __str__(self):
    return self.item_name


class MarketItems(models.Model):
  item = models.ForeignKey(
    Item,
    on_delete = models.SET_NULL,
    null=True
  )
  item_price = models.PositiveIntegerField(
    default = 0
  )


class Market(models.Model):
  items = models.ForeignKey(
    MarketItems,
    on_delete = models.SET_NULL,
    null = True
  )
  name = models.CharField(
    max_length = 128
  )
  latitude = models.FloatField()
  longitude = models.FloatField()
  street_address = models.TextField()
  updated_at = models.DateTimeField(
    auto_now_add = True
  )

  def __str__(self):
    return self.name