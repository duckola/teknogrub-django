from django import forms
from .models import MenuItem, Category

class MenuItemForm(forms.ModelForm):
    # These fields aren't in MenuItem, but we use them to update the Inventory model
    current_stock = forms.IntegerField(min_value=0, initial=100, required=True, label="Current Stock")
    threshold_level = forms.IntegerField(min_value=0, initial=20, required=True, label="Low Stock Threshold")

    class Meta:
        model = MenuItem
        fields = [
            'name',
            'category',
            'canteen',
            'price',
            'description',
            'ingredients',
            'image_url',
            'is_available'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the dish...'}),
            'ingredients': forms.TextInput(attrs={'placeholder': 'e.g. Beef, Onions, Soy Sauce'}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']