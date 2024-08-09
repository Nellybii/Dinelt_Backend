from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
import os

class User(AbstractUser):
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

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

    def save(self, *args, **kwargs):
        if not self.image or not hasattr(self.image, 'path'):  # If no image is provided
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics/default.jpg')
            if os.path.exists(default_image_path):
                with open(default_image_path, 'rb') as f:
                    self.image.save('default.jpg', File(f), save=False)
        super(User, self).save(*args, **kwargs)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="post_images", default="default.jpg")
    created_at = models.DateTimeField(auto_now_add=True)

class Story(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stories')
    content = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="story_images", default="default.jpg")
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'path'):
            im = Image.open(self.image)
            im.thumbnail((500, 500))  # Example size for stories
            im.save(self.image.path)
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    bio = models.CharField(max_length=300)
    image = models.ImageField(upload_to="profile_images", default="default.jpg")
    posts = models.ManyToManyField(Post, blank=True, related_name='profiles')
    stories = models.ManyToManyField(Story, blank=True, related_name='profiles')
    followers = models.ManyToManyField(User, blank=True, related_name='following')
    following = models.ManyToManyField(User, blank=True, related_name='followers')

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'path'):
            im = Image.open(self.image)
            im.thumbnail((100, 100))  
            im.save(self.image.path)
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username)
