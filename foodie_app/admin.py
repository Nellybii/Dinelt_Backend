from django.contrib import admin
from foodie_app.models import User, Profile, Restaurant, Order, OrderItem, Reservation

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'image', 'followers', 'following')
    list_editable = ('bio',)
    search_fields = ('user__username', 'bio')

# @admin.register(Restaurant)
# class RestaurantAdmin(admin.ModelAdmin):
#     list_display = ('name', 'country', 'city')
#     search_fields = ('name', 'country', 'city')

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('user', 'restaurant', 'total_price', 'status')
#     list_filter = ('status',)
#     search_fields = ('user__email', 'restaurant__name')

# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('order', 'menu_item', 'quantity', 'price')

# @admin.register(Reservation)
# class ReservationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'restaurant', 'reservation_date')
#     search_fields = ('user__email', 'restaurant__name')
