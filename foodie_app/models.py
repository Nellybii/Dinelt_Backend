from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.utils.translation import gettext_lazy as _


import logging
from django.utils import timezone


logger = logging.getLogger(__name__)




FOOD_CATEGORY_CHOICES = [
    ('appetizer', _('Appetizer')),
    ('main_course', _('Main Course')),
    ('dessert', _('Dessert')),
    ('beverage', _('Beverage')),
]


RESERVATION_TYPE_CHOICES = [
    ('conference_room', _('Conference Room')),
    ('meeting_table', _('Meeting Table')),
]


STATUS_CHOICES = [
    ('Pending', _('Pending')),
    ('Completed', _('Completed')),
    ('Cancelled', _('Cancelled')),
]


class User(AbstractUser):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    image = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    is_business_owner = models.BooleanField(default=False, null=False)


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


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    bio = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="user_images", blank=True, null=True)
    followers_number = models.ManyToManyField(
        'self', symmetrical=False, related_name='following_profiles', blank=True
    )
    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='follower_profiles', blank=True,
    )
    posts = models.ManyToManyField('Post', related_name='profile_posts', blank=True)
    stories = models.ManyToManyField('Story', related_name='profile_stories', blank=True)
    is_business_owner = models.BooleanField(default=False, null=False)


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    image = models.ImageField(upload_to="post_images", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField('Comments', blank=True, related_name="post_comments")
    likes = models.IntegerField(default=0)


class Story(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stories')
    content = models.TextField()
    image = models.ImageField(upload_to="story_images", blank=True, null=True)
    comments = models.ManyToManyField('Comments', blank=True, related_name="story_comments")
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)  


    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = self.created_at + timedelta(hours=24)  
        super().save(*args, **kwargs)


class Comments(models.Model):
    content = models.TextField(blank=True, max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')


class Restaurant(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_restaurants')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='restaurant_images', blank=True, null=True)
    description = models.TextField(blank=True)
   
    @property
    def managers(self):
        return User.objects.filter(manager__restaurant=self)
   
    def __str__(self):
        return self.name


class RestaurantReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.restaurant.name}"


class Food(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=FOOD_CATEGORY_CHOICES, null=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='foods')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=False)


    def __str__(self):
        return self.name


class ReservationCategory(models.Model):
    name = models.CharField(max_length=255)
    reservation_type = models.CharField(max_length=20, choices=RESERVATION_TYPE_CHOICES)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reservation_categories')
   
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    order_time = models.DateTimeField(auto_now_add=True)
    estimated_delivery_time = models.DateTimeField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_total_price(self):
        # Calculate the total price by summing the price of all associated OrderItems
        return sum(item.food.price * item.quantity for item in self.order_items.all())

    def save(self, *args, **kwargs):
        # Calculate the total price before saving the order
        if self.pk:  # Ensure the Order has been saved and has a primary key
            self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.food.name} in Order {self.order.id}"
    
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        total = sum(item.total_price for item in self.cart_items.all())
        return round(total, 2)

    def __str__(self):
        return f"Cart for {self.user.username} (ID: {self.id})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    food = models.ForeignKey('Food', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return round(self.quantity * self.food.price, 2)

    def __str__(self):
        return f"{self.quantity}x {self.food.name} in Cart {self.cart.id}"
    

class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)
    reservation_date = models.DateTimeField()
    number_of_people = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    reservation_type = models.CharField(max_length=50, choices=RESERVATION_TYPE_CHOICES)


    def __str__(self):
        return f"Reservation for {self.user.username} (ID: {self.id})"




class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accommodation = models.ForeignKey('Accommodation', on_delete=models.CASCADE)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField()
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)


    def __str__(self):
        return f"Booking {self.id} by {self.user.username} from {self.check_in_date} to {self.check_out_date}"




class Accommodation(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='accommodation_images', blank=True, null=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.name


class Manager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date_assigned = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} is a manager for {self.restaurant.name}"
   
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(
            user=instance,
            username=instance.username,
            defaults={'image': instance.image}
        )
