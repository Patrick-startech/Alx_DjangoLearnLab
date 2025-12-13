# Create your models here.
# notifications/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='actions'
    )
    verb = models.CharField(max_length=64)  # e.g., 'followed', 'liked', 'commented'
    # Generic target: can be a Post, Comment, or User, etc.
    target_content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    target_object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    timestamp = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.actor} {self.verb} {self.target} → {self.recipient}'
