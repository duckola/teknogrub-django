from django.urls import path
from . import views

urlpatterns = [
    # --- Public Side ---
    # http://127.0.0.1:8000/menu/
    path('', views.menu_view, name='menu'),

    # http://127.0.0.1:8000/menu/favorites/
    path('favorites/', views.favorites_view, name='favorites'),

    # --- Staff / Admin Side ---
    # Inventory Management
    # http://127.0.0.1:8000/menu/staff/inventory/
    path('staff/inventory/', views.inventory_list, name='inventory'),

    # Add Item
    # http://127.0.0.1:8000/menu/staff/inventory/add/
    path('staff/inventory/add/', views.add_edit_item, name='add_item'),

    # Edit Item
    # http://127.0.0.1:8000/menu/staff/item/edit/5/
    path('staff/item/edit/<int:item_id>/', views.add_edit_item, name='edit_item'),

    # Delete Item
    path('staff/item/delete/<int:item_id>/', views.delete_item, name='delete_item'),

    # Category Management
    # http://127.0.0.1:8000/menu/staff/categories/
    path('staff/categories/', views.category_list, name='categories'),

    # Add Category
    path('staff/categories/add/', views.add_edit_category, name='add_category'),

    # Edit Category
    # http://127.0.0.1:8000/menu/staff/categories/edit/1/
    path('staff/categories/edit/<int:cat_id>/', views.add_edit_category, name='edit_category'),

    # Delete Category
    path('staff/categories/delete/<int:cat_id>/', views.delete_category, name='delete_category'),
]