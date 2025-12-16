from django.db import models
from Menu.models import MenuItem
class Promo(models.Model):
    title = models.CharField(max_length=100)
    discount_percent = models.IntegerField()
    applicable_items = models.ManyToManyField(MenuItem, related_name='promos')
    is_active = models.BooleanField(default=True)