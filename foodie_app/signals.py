from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.get_or_create(user=instance, defaults={'username': instance.username})
            logger.info(f"Profile created for user {instance.username}")
        except Exception as e:
            logger.error(f"Failed to create profile for user {instance.username}: {e}")
