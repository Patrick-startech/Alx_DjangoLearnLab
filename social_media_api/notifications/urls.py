# notifications/urls.py
from django.urls import path
from .views import NotificationListView, NotificationMarkReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/mark-read/', NotificationMarkReadView.as_view(), name='notifications-mark-read'),
]
