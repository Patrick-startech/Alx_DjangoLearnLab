# Create your views here.
from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.select_related('actor').filter(recipient=self.request.user)
        show_unread = self.request.query_params.get('unread', None)
        if show_unread in ('1', 'true', 'True'):
            qs = qs.filter(unread=True)
        return qs

class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Bulk mark all as read for current user
        Notification.objects.filter(recipient=self.request.user, unread=True).update(unread=False)
        # Return latest notification just for response context (optional pattern)
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp').first()
