from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserPaymentMethod
from django.contrib import messages  # Optional: Use messages for user feedback
from django.db import connection

@login_required
def add_payment_method(request):
    if request.method == "POST":
        try:
            method_type = request.POST.get('method_type')

            # 1. Reset defaults first
            if request.POST.get('is_default') == 'true':
                UserPaymentMethod.objects.filter(user=request.user).update(is_default=False)

            with connection.cursor() as cursor:
                if method_type == 'GCash':
                    gcash_number = request.POST.get('gcash_number')
                    if gcash_number:
                        cursor.callproc('CreateUserPaymentMethod', [
                            request.user.id,
                            'GCash',
                            None,
                            gcash_number,
                            None,
                            None,
                            True
                        ])
                elif method_type == 'Card':
                    full_card = request.POST.get('card_number', '')
                    expiry = request.POST.get('expiry')
                    if full_card and expiry:
                        cursor.callproc('CreateUserPaymentMethod', [
                            request.user.id,
                            'Card',
                            None,
                            None,
                            full_card[-4:],
                            expiry,
                            True
                        ])
            return redirect('settings')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('settings')

    return redirect('settings')

@login_required
def delete_payment_method(request, method_id):
    try:
        with connection.cursor() as cursor:
            cursor.callproc('DeleteUserPaymentMethod', [method_id])
        return redirect('settings')
    except Exception as e:
        messages.error(request, str(e))
        return redirect('settings')