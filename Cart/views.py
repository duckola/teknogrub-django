from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static

from .models import Cart, CartItem
from Menu.models import MenuItem
import json


def get_csrf_token(request):
    return request.COOKIES.get('csrftoken')


@login_required
def add_to_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')

            cart, _ = Cart.objects.get_or_create(user=request.user)
            item = get_object_or_404(MenuItem, pk=item_id)

            if cart.items.exists():
                if cart.items.first().menu_item.canteen != item.canteen:
                    return JsonResponse({'status': 'error', 'message': 'Cannot mix items from different canteens.'},
                                        status=400)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)
            if not created:
                cart_item.quantity += 1
            cart_item.save()

            return JsonResponse({'status': 'success', 'cart_count': cart.items.count()})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


@login_required
def get_cart_data(request):
    """Returns JSON data of cart contents, prices, and total for the JS sidebar."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items_data = []
    total = 0

    for ci in cart.items.all().select_related('menu_item'):
        cost = ci.menu_item.price * ci.quantity
        total += cost
        items_data.append({
            'id': ci.menu_item.pk,
            'name': ci.menu_item.name,
            'price': float(ci.menu_item.price),
            'qty': ci.quantity,
            'subtotal': cost,
            'img': ci.menu_item.image_url.url if ci.menu_item.image_url else static('images/food.png')
        })

    return JsonResponse({'items': items_data, 'total': float(total)})

@login_required
def change_qty(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            change = data.get('change')

            cart = get_object_or_404(Cart, user=request.user)
            item = get_object_or_404(MenuItem, pk=item_id)
            cart_item = get_object_or_404(CartItem, cart=cart, menu_item=item)

            cart_item.quantity += change

            if cart_item.quantity <= 0:
                cart_item.delete()
                return JsonResponse({'status': 'deleted'})

            cart_item.save()
            return JsonResponse({'status': 'success', 'new_qty': cart_item.quantity})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)