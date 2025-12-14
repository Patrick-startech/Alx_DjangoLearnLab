# blog/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for {sender.__name__}: {instance.username}")
    else:
         # kwargs contains 'update_fields' if save() was called with update_fields
        instance.profile.save(update_fields=kwargs.get('update_fields', None))
