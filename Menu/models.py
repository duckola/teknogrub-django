from django.db import models
from django.conf import settings
from Canteen.models import Canteen


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self): return self.category_name


class MenuItem(models.Model):
    canteen = models.ForeignKey(Canteen, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    ingredients = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.ImageField(upload_to='food_imgs/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self): return f"{self.name} ({self.canteen.name})"


class Inventory(models.Model):
    item = models.OneToOneField(MenuItem, on_delete=models.CASCADE, related_name='inventory')
    current_stock = models.IntegerField(default=0)
    threshold_level = models.IntegerField(default=10)


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)