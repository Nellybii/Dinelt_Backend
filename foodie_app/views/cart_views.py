# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import permissions, status
# from foodie_app.models import Cart, CartItem, Food
# from foodie_app.serializer import CartSerializer
# from django.shortcuts import get_object_or_404

# class CartCreateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         cart_items_data = request.data.get('cart_items', [])

#         if not isinstance(cart_items_data, list):
#             return Response({"detail": "Cart items must be a list."}, status=status.HTTP_400_BAD_REQUEST)

#         if not cart_items_data:
#             return Response({"detail": "At least one cart item is required."}, status=status.HTTP_400_BAD_REQUEST)

#         carts = Cart.objects.filter(user=request.user)
#         cart = carts.first() if carts.exists() else Cart.objects.create(user=request.user)

#         for item in cart_items_data:
#             food_id = item.get('food_id')
#             quantity = item.get('quantity')

#             if not food_id or not quantity:
#                 return Response({"detail": "Each cart item must include food_id and quantity."}, status=status.HTTP_400_BAD_REQUEST)

#             food = get_object_or_404(Food, id=food_id)

#             if quantity <= 0:
#                 return Response({"detail": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

#             price = food.price

#             CartItem.objects.update_or_create(
#                 cart=cart,
#                 food=food,
#                 defaults={'quantity': quantity, 'price': price}
#             )

#         cart_serializer = CartSerializer(cart)
#         return Response(cart_serializer.data, status=status.HTTP_201_CREATED)

# class CartRetrieveView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         cart = get_object_or_404(Cart, user=request.user)
#         serializer = CartSerializer(cart)
#         return Response(serializer.data)

# class CartUpdateView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def put(self, request):
#         cart_items_data = request.data.get('cart_items', [])

#         if not isinstance(cart_items_data, list):
#             return Response({"detail": "Cart items must be a list."}, status=status.HTTP_400_BAD_REQUEST)

#         if not cart_items_data:
#             return Response({"detail": "At least one cart item is required."}, status=status.HTTP_400_BAD_REQUEST)

#         cart = get_object_or_404(Cart, user=request.user)
#         total_price = 0

#         for item in cart_items_data:
#             food_id = item.get('food_id')
#             quantity = item.get('quantity')

#             if not food_id or not quantity:
#                 return Response({"detail": "Each cart item must include food_id and quantity."}, status=status.HTTP_400_BAD_REQUEST)

#             food = get_object_or_404(Food, id=food_id)

#             if quantity <= 0:
#                 return Response({"detail": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

#             price = food.price
#             total_price += price * quantity

#             CartItem.objects.update_or_create(
#                 cart=cart,
#                 food=food,
#                 defaults={'quantity': quantity, 'price': price}
#             )

#         cart.total_price = total_price
#         cart.save()

#         cart_serializer = CartSerializer(cart)
#         return Response(cart_serializer.data, status=status.HTTP_200_OK)

# class CartDeleteView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def delete(self, request):
#         cart = get_object_or_404(Cart, user=request.user)
#         cart.cartitem_set.all().delete()  # Remove all cart items
#         return Response(status=status.HTTP_204_NO_CONTENT)
