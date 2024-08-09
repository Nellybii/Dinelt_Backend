from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from PIL import Image

class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200, blank=True)
    username = models.CharField(max_length=100)
    image = models.ImageField(upload_to='user_images', default='default.jpg', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'username'

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user'
    )

    def get_profile(self):
        profile, created = Profile.objects.get_or_create(user=self)
        return profile

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200)
    bio = models.CharField(max_length=300)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'path'):
            im = Image.open(self.image)
            im.thumbnail((100, 100))  
            im.save(self.image.path)
        super().save(*args, **kwargs)

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
