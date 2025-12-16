from Order.models import Order
from django.db.models import Count, Q

def order_counts(request):
    if request.user.is_authenticated and (request.user.is_superuser or (request.user.role and request.user.role.role_name in ['Staff', 'Admin'])):
        counts = Order.objects.aggregate(
            pending=Count('id', filter=Q(status='Pending')),
            preparing=Count('id', filter=Q(status='Preparing')),
            ready=Count('id', filter=Q(status='Ready')),
            completed=Count('id', filter=Q(status='Completed'))
        )
        return {'counts': counts}
    return {}
