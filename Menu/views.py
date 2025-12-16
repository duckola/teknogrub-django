from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from .models import MenuItem, Category, Inventory, Favorite
from Canteen.models import Canteen
from .forms import MenuItemForm, CategoryForm
from Promo.models import Promo
from Menu.models import MenuItem # Ensure MenuItem is imported
from django.db.models import Q, Count
from django.db import connection
import json


# --- Helpers ---
def is_staff(u):
    return u.is_staff or (u.role and u.role.role_name in ['Staff', 'Admin'])


# --- User Views ---

@login_required
def set_canteen(request):
    """Handles changing the active canteen via the sidebar dropdown."""
    if request.method == "POST":
        cid = request.POST.get('canteen_id')
        try:
            canteen = Canteen.objects.get(pk=cid)
            request.session['canteen_id'] = int(cid)
            request.session['canteen_name'] = canteen.name
        except Canteen.DoesNotExist:
            pass
    return redirect(request.META.get('HTTP_REFERER', 'menu'))


@login_required
def menu_view(request):
    """Displays the main menu, filtered by Canteen and Category."""

    # 1. Get Canteen
    cid = request.session.get('canteen_id')
    if not cid:
        # Set default canteen if session is empty
        first = Canteen.objects.first()
        if first:
            cid = first.pk
            request.session['canteen_id'] = first.pk
            request.session['canteen_name'] = first.name

    cat_filter = request.GET.get('category', 'All')
    all_canteens = Canteen.objects.all()
    categories = Category.objects.all()

    # 2. Base Item Query
    items = MenuItem.objects.filter(canteen_id=cid, is_available=True)

    # 3. Search/Filter Logic (If you added a search bar to the menu template)
    search_query = request.GET.get('q')
    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # 4. Category Filter
    if cat_filter != 'All':
        items = items.filter(category__category_name=cat_filter)

    # 5. Favorite Flag (Required for star icon consistency)
    user_fav_ids = Favorite.objects.filter(user=request.user).values_list('item_id', flat=True)
    for i in items:
        i.is_favorite = i.id in user_fav_ids
        if i.image_url:
            i.image_url = i.image_url.url
        else:
            i.image_url = ''


    context = {
        'menu_items': items,
        'categories': categories,
        'active_category': cat_filter,
        'canteens_list': all_canteens,
        'popular_items': items.order_by('?')[:4]
    }
    return render(request, 'menu/menu.html', context)


@login_required
def toggle_favorite(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, item=item)

    if not created:
        fav.delete()
        status = 'removed'
    else:
        status = 'added'

    # Redirect if on the favorites page to refresh the state
    if request.META.get('HTTP_REFERER', '').endswith('/favorites/'):
        return JsonResponse({'status': 'redirect', 'url': '/favorites/'})

    return JsonResponse({'status': status})


@login_required
def favorites_view(request):
    favs = Favorite.objects.filter(user=request.user).select_related('item')
    items = []
    for f in favs:
        f.item.is_favorite = True
        items.append(f.item)

    # Ensure canteens list is passed for the dropdown to show up
    return render(request, 'menu/favorites.html', {
        'menu_items': items,
        'canteens_list': Canteen.objects.all()
    })


@login_required
def promos_view(request):
    # FIX: Use the correct related name (should be 'promos') OR use the default (related_name='promos_set')
    # We will use the default relationship name to be safe if you didn't define a related_name on the M2M field.
    promos = Promo.objects.filter(is_active=True).prefetch_related('applicable_items')

    # NOTE: If the above still fails, change prefetch_related('applicable_items') to prefetch_related('promo') or 'promos_set'

    return render(request, 'menu/promos.html', {'promos': promos, 'canteens_list': Canteen.objects.all()})

# --- Admin/Staff Logic ---

def is_staff(u):
    return u.is_staff or (u.role and u.role.role_name in ['Staff', 'Admin'])


@user_passes_test(is_staff)
def inventory_list(request):
    # Ensure inventory list is populated via database
    items = Inventory.objects.select_related('item').all()
    return render(request, 'menu/inventory.html', {'inventory_list': items})


@user_passes_test(is_staff)
def add_edit_item(request, item_id=None):
    item = get_object_or_404(MenuItem, pk=item_id) if item_id else None
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            try:
                with connection.cursor() as cursor:
                    if item:
                        cursor.callproc('UpdateMenuItem', [
                            item.id,
                            form.cleaned_data['canteen'].id,
                            form.cleaned_data['category'].id,
                            form.cleaned_data['name'],
                            form.cleaned_data['description'],
                            form.cleaned_data['ingredients'],
                            form.cleaned_data['price'],
                            form.cleaned_data['image_url'],
                            form.cleaned_data['is_available']
                        ])
                    else:
                        cursor.callproc('CreateMenuItem', [
                            form.cleaned_data['canteen'].id,
                            form.cleaned_data['category'].id,
                            form.cleaned_data['name'],
                            form.cleaned_data['description'],
                            form.cleaned_data['ingredients'],
                            form.cleaned_data['price'],
                            form.cleaned_data['image_url'],
                            form.cleaned_data['is_available']
                        ])
                        item_id = cursor.fetchone()[0]
                
                mi = MenuItem.objects.get(pk=item_id)
                Inventory.objects.update_or_create(item=mi, defaults={
                    'current_stock': form.cleaned_data['current_stock'],
                    'threshold_level': form.cleaned_data['threshold_level']
                })
                return redirect('inventory')
            except Exception as e:
                # Handle database errors
                form.add_error(None, str(e))
    else:
        initial = {}
        if item and hasattr(item, 'inventory'):
            initial = {'current_stock': item.inventory.current_stock, 'threshold_level': item.inventory.threshold_level}
        form = MenuItemForm(instance=item, initial=initial)
    return render(request, 'menu/admin_add_item.html', {'form': form, 'item': item})


@user_passes_test(is_staff)
def delete_item(request, item_id):
    get_object_or_404(MenuItem, pk=item_id).delete()
    return redirect('inventory')


@user_passes_test(is_staff)
def category_list(request):
    cats = Category.objects.all()
    for c in cats: c.item_count = MenuItem.objects.filter(category=c).count()
    return render(request, 'menu/categories.html', {'categories': cats})


@user_passes_test(is_staff)
def add_edit_category(request, cat_id=None):
    cat = get_object_or_404(Category, pk=cat_id) if cat_id else None
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=cat)
        if form.is_valid():
            c = form.save()
            # Logic for assigned items (handling the dual-list move)
            assigned = request.POST.getlist('assigned_items')
            MenuItem.objects.filter(category=c).exclude(id__in=assigned).update(category=None)
            MenuItem.objects.filter(id__in=assigned).update(category=c)
            return redirect('categories')
    else:
        form = CategoryForm(instance=cat)

    assigned = MenuItem.objects.filter(category=cat).select_related('inventory') if cat else []
    available = MenuItem.objects.exclude(category=cat).select_related('inventory') if cat else MenuItem.objects.filter(
        category__isnull=True)

    return render(request, 'menu/admin_add_category.html',
                  {'form': form, 'assigned_items': assigned, 'available_items': available, 'category': cat})


@user_passes_test(is_staff)
def delete_category(request, cat_id):
    get_object_or_404(Category, pk=cat_id).delete()
    return redirect('categories')