from django.http import JsonResponse
from .models import Notification
def get_notifications(request):
    notes = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    return JsonResponse({'count': notes.count(), 'notifications': list(notes.values('id', 'title', 'message'))})
def mark_read(request, notif_id):
    Notification.objects.filter(pk=notif_id).update(is_read=True)
    return JsonResponse({'status':'success'})