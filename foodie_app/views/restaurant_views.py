from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from foodie_app.models import Restaurant, OrderItem, Reservation
from foodie_app.serializer import RestaurantSerializer, ReservationSerializer, OrderItemSerializer

class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view the list of restaurants

class RestaurantDetailView(generics.RetrieveAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can view restaurant details

class RestaurantCreateView(generics.CreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RestaurantUpdateView(generics.UpdateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser]  # Only admin can update a restaurant

class RestaurantDeleteView(generics.DestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminUser]  # Only admin can delete a restaurant

class ReservationCreateView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can make reservations

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemListView(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]  # Only authenticated users can create order items
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
