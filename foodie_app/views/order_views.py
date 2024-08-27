from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from foodie_app.models import Order, Food, OrderItem
from foodie_app.serializer import OrderSerializer
from django.shortcuts import get_object_or_404

class OrderCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get the list of order items from the request data
        order_items_data = request.data.get('order_items', [])

        # Validate that order_items_data is a list
        if not isinstance(order_items_data, list):
            return Response({"detail": "Order items must be a list."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Ensure there is at least  one order item
        if not order_items_data:
            return Response({"detail": "At least one order item is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize total price
        total_price = 0
        
        # Create a new Order instance but do not save yet
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            # Calculate total price
            for item in order_items_data:
                food_id = item.get('food_id')
                quantity = item.get('quantity')

                # Validate food existence
                food = get_object_or_404(Food, id=food_id)

                # Validate quantity
                if quantity <= 0:
                    return Response({"detail": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

                # Calculate price
                price = food.price
                total_price += price * quantity

            # Save the order with the total price
            order = order_serializer.save(user=request.user, total_price=total_price)

            # Create OrderItem instances
            for item in order_items_data:
                food_id = item.get('food_id')
                quantity = item.get('quantity')
                food = get_object_or_404(Food, id=food_id)
                price = food.price
                
                OrderItem.objects.create(
                    order=order,
                    food=food,
                    quantity=quantity,
                    price=price
                )
            
            # Return the serialized order data
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)

        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderRetrieveUpdateDestroyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Retrieve all orders related to the currently logged-in user
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
