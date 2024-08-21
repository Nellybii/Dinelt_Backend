from django.contrib import admin
from django.utils.html import format_html
from foodie_app.models import User, Profile, Restaurant, Order, OrderItem, Reservation

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'full_name', 'phone_number']
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_active']
    ordering = ['username']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'bio', 'profile_image', 'get_followers_count', 'get_following_count')
    list_editable = ('bio',)
    search_fields = ('user__username', 'bio')
    ordering = ('user',)

    def get_full_name(self, obj):
        return obj.user.full_name
    get_full_name.short_description = 'Full Name'

    def profile_image(self, obj):
        if obj.user.image:
            return format_html('<img src="{}" width="50" height="50"/>', obj.user.image.url)
        return 'No image'
    profile_image.short_description = 'Profile Image'

    def get_followers_count(self, obj):
        return obj.followers.count()
    get_followers_count.short_description = 'Followers Count'

    def get_following_count(self, obj):
        return obj.following.count()
    get_following_count.short_description = 'Following Count'

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'city', 'country', 'phone_number')
    search_fields = ('name', 'address', 'city', 'country')
    list_filter = ('city', 'country')
    ordering = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'total_price', 'created_at', 'status')
    search_fields = ('user__username', 'restaurant__name', 'status')
    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'food', 'price', 'quantity')  # Ensure this matches your OrderItem model fields
    search_fields = ('order__id', 'food__name')
    list_filter = ('order', 'food')
    ordering = ('order',)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'restaurant', 'reservation_date', 'number_of_people')
    search_fields = ('user__username', 'restaurant__name')
    list_filter = ('reservation_date',)
    ordering = ('-reservation_date',)

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Reservation, ReservationAdmin)
