from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from PIL import Image
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files import File
from datetime import timedelta
import os

class User(AbstractUser):
    password = models.CharField(max_length=128)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False)
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
    expires_at = models.DateTimeField(null=True, blank=True)  
# followers
# reviews
# Comments  
# food category(3)
# reservations category (3)
# cart
# bookings


    def save(self, *args, **kwargs):
        if not self.is_superuser:
            if not self.image or not hasattr(self.image, 'path'):  
                default_image_path = os.path.join(settings.MEDIA_ROOT, 'profile_pics/default.jpg')
                if os.path.exists(default_image_path):
                    with open(default_image_path, 'rb') as f:
                        self.image.save('default.jpg', File(f), save=False)
        super(User, self).save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    bio = models.CharField(max_length=300)
    image = models.ImageField(upload_to="user_images", default="default.jpg")
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    posts = models.ManyToManyField('Post', related_name='Post', blank=True)
    stories=models.ManyToManyField('Story', related_name='Story', blank=True)

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100) 
    country = models.CharField(max_length=100)  
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='restaurant_images', default='default.jpg')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu_images', default='default.jpg')

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField()
    number_of_people = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)

    def __str__(self):
        return f"Reservation {self.id} by {self.user.username} on {self.reservation_date}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance, username=instance.username)

