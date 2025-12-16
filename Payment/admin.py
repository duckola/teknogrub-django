from django.contrib import admin
from .models import Payment, UserPaymentMethod

# Register the transaction logs
admin.site.register(Payment)

# Register the saved user methods
admin.site.register(UserPaymentMethod)