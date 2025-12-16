from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Inventory)

# admin.site.register(AddOn)
# admin.site.register(MenuItemAddOn)
# admin.site.register(MenuItemCategories)