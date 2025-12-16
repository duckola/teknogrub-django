from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from User import views as user_views
from Menu import views as menu_views
from Cart import views as cart_views
from Order import views as order_views
from Notification import views as notif_views
from Payment import views as payment_views

urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('', user_views.login_view, name='login'),
                  path('signup/', user_views.signup_view, name='signup'),
                  path('logout/', user_views.logout_view, name='logout'),
                  path('settings/', user_views.settings_view, name='settings'),

                  path('menu/', menu_views.menu_view, name='menu'),
                  path('favorites/', menu_views.favorites_view, name='favorites'),
                  path('promos/', menu_views.promos_view, name='promos'),
                  path('history/', order_views.history_view, name='history'),
                  path('reorder/<int:order_id>/', order_views.reorder, name='reorder'),

                  path('set_canteen/', menu_views.set_canteen, name='set_canteen'),
                  path('menu/favorite/toggle/<int:item_id>/', menu_views.toggle_favorite, name='toggle_favorite'),
                  path('api/cart/add/', cart_views.add_to_cart, name='add_to_cart'),
                  path('api/cart/update/', cart_views.get_cart_data, name='get_cart'),
                  path('api/cart/change_qty/', cart_views.change_qty, name='change_qty'),
                  path('api/cart/checkout/', order_views.checkout, name='checkout'),
                  path('api/notifications/get/', notif_views.get_notifications, name='get_notifications'),
                  path('api/notifications/read/<int:notif_id>/', notif_views.mark_read, name='mark_read'),

                  path('payment/add/', payment_views.add_payment_method, name='add_payment_method'),
                  path('payment/delete/<int:method_id>/', payment_views.delete_payment_method, name='delete_payment'),

                  path('staff/dashboard/', order_views.admin_dashboard, name='admin_dashboard'),
                  path('staff/orders/', order_views.staff_orders, name='staff_orders'),
                  path('staff/order/update/<int:order_id>/', order_views.update_order_status,
                       name='update_order_status'),

                  path('manage/inventory/', menu_views.inventory_list, name='inventory'),
                  path('manage/inventory/add/', menu_views.add_edit_item, name='add_item'),
                  path('manage/inventory/edit/<int:item_id>/', menu_views.add_edit_item, name='edit_item'),
                  path('manage/inventory/delete/<int:item_id>/', menu_views.delete_item, name='delete_item'),

                  path('manage/categories/', menu_views.category_list, name='categories'),
                  path('manage/categories/add/', menu_views.add_edit_category, name='add_category'),
                  path('manage/categories/edit/<int:cat_id>/', menu_views.add_edit_category, name='edit_category'),
                  path('manage/categories/delete/<int:cat_id>/', menu_views.delete_category, name='delete_category'),

                  path('settings/password/change/',
                       auth_views.PasswordChangeView.as_view(template_name='User/password_change.html'),
                       name='password_change'),
                  path('settings/password/change/done/', auth_views.PasswordChangeDoneView.as_view(),
                       name='password_change_done'),
                  path('history/reorder/<int:old_order_id>/', order_views.reorder_view, name='reorder_item'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)