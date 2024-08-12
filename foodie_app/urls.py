from django.urls import path
from .views import User_views, Post_views, Story_views, restaurant_views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', User_views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', User_views.RegisterView.as_view(), name='auth_register'),
    path('profile/', User_views.ProfileRetrieveUpdateDestroyView.as_view(), name='user_profile'),
    path('profile/update/', User_views.ProfileUpdate.as_view(), name='update_profile'),
    path('test/', User_views.testEndPoint, name='test'),
    path('', User_views.getRoutes),
    path('posts/', Post_views.PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', Post_views.PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
    path('stories/', Story_views.StoryListCreate.as_view(), name='stories-list-create'),
    path('stories/<int:pk>/', Story_views.StoryRetrieveUpdateDestroyView.as_view(), name='story-detail'),
    path('restaurants/', restaurant_views.RestaurantListView.as_view(), name='restaurant_list'),
    path('restaurants/create/', restaurant_views.RestaurantCreateView.as_view(), name='restaurant_list'),
    path('restaurants/<int:pk>/', restaurant_views.RestaurantDetailView.as_view(), name='restaurant_detail'),
    path('orders/', restaurant_views.OrderItemListView.as_view(), name='order_create'),
    path('reservations/', restaurant_views.ReservationCreateView.as_view(), name='reservation_create'),
]

