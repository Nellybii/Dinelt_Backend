from django.urls import path
from .views import User_views, Post_views, Story_views, restaurant_views, order_views, cart_views, food_views, accomodation_views, reservation_views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', User_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', User_views.RegisterView.as_view(), name='auth_register'),
    path('templates/u/profile.html/', User_views.ProfileRetrieveUpdateDestroyView.as_view(), name='user_profile'),
    path('templates/u/profile.html/update/', User_views.ProfileRetrieveUpdateDestroyView.as_view(), name='update_profile'),
    path('profile/<str:username>/', User_views.ProfileDetailView.as_view(), name='profile-detail'),
    path('test/', User_views.testEndPoint, name='test'),
    path('', User_views.getRoutes),
    path('posts/', Post_views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', Post_views.PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('stories/', Story_views.StoryListCreate.as_view(), name='stories-list-create'),
    path('stories/<int:pk>/', Story_views.StoryRetrieveUpdateDestroyView.as_view(), name='story-detail'),
    path('restaurants/', restaurant_views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/create/', restaurant_views.RestaurantCreateView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', restaurant_views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('restaurants/<int:pk>/update/', restaurant_views.RestaurantUpdateView.as_view(), name='restaurant-update'),
    path('restaurants/<int:pk>/delete/', restaurant_views.RestaurantDeleteView.as_view(), name='restaurant-delete'),
    path('food/', food_views.FoodListView.as_view(), name='food-list'),
    path('food/create/', food_views.FoodCreateView.as_view(), name='food-create'),
    path('food/<int:pk>/', food_views.FoodDetailView.as_view(), name='food-detail'),
    path('food/<int:pk>/update/', food_views.FoodUpdateView.as_view(), name='food-update'),
    path('food/<int:pk>/delete/', food_views.FoodDeleteView.as_view(), name='food-delete'),
    path('orders/', order_views.OrderListView.as_view(), name='order-list'),  # List all orders
    path('orders/create/', order_views.OrderCreateView.as_view(), name='order-create'),
    path('orders/<int:order_id>/', order_views.OrderRetrieveUpdateDestroyView.as_view(), name='order-detail'),
    path('cart/', cart_views.CartRetrieveView.as_view(), name='cart-create-or-update'),
    path('cart/add/', cart_views.CartCreateOrUpdateView.as_view(), name='add-to-cart'),
    path('cart/update/<int:pk>/', cart_views.CartUpdateView.as_view(), name='remove-from-cart'),
    path('cart/delete/<int:pk>/', cart_views.CartDeleteView.as_view(), name='remove-from-cart'),
    path('accommodation/create/', accomodation_views.AccommodationCreateView.as_view(), name='accommodation-create'),
    path('accommodation/', accomodation_views.AccommodationListView.as_view(), name='accommodation-list'),
    path('accommodation/<int:pk>/', accomodation_views.AccommodationDetailView.as_view(), name='accommodation-detail'),
    path('accommodation/<int:pk>/update/', accomodation_views.AccommodationUpdateView.as_view(), name='accommodation-update'),
    path('accommodation/<int:pk>/delete/', accomodation_views.AccommodationDeleteView.as_view(), name='accommodation-delete'),
    path('bookings/', accomodation_views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', accomodation_views.BookingRetrieveUpdateDestroyView.as_view(), name='booking-detail'),
    path('reservations/', reservation_views.ReservationListCreateAPIView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', reservation_views.ReservationRetrieveUpdateDestroyAPIView.as_view(), name='reservation-detail')
]
 # followers
# reviews
# Comments  
# food category(3)
# reservations category (3)
# cart
# bookings

