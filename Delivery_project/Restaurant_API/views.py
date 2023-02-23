from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

# Models
from .models import *

# Serializers
from .serializers import *

# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

class MenuitemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuitemSerializer
    filterset_fields = ['price']
    search_fields = ['title']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != "GET":
            permission_classes = [IsAuthenticated]

            return [permission() for permission in permission_classes]
        
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuitemSerializer


class CartView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all().filter(user=self.request.user)
    
    def delete(self):
        Cart.objects.all().filter(user=self.request.user).delete()
        return Response("Deleted OK!")



class OrderView(generics.ListCreateAPIView):
    queryset = Oreder.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Oreder.objects.all()
        elif self.request.user.groups.count() == 0:
            return Oreder.objects.all().filter(user=self.request.user)
        elif self.request.user.groups.filter(name='delivery_crew').exists():
            return Oreder.objects.all().filter(delivery_crew=self.request.user)
        else:
            return Oreder.objects.all()
        

    def create(self, *args, **kwargs):
        menuitem_count = Cart.objects.all().filter(user=self.request.user).count()
        if menuitem_count == 0:
            return Response({"message": "No item in cart"})
        
        data = self.request.data.copy()
        total = self.get_total_price(self.request.user)
        data['total'] = total
        data['user'] = self.request.user.id
        order_serializer = OrderSerializer(data=data)
    
        if order_serializer.is_valid():
            order = order_serializer.save()

            items = Cart.objects.all().filter(user=self.request.user).all()

            for item in items.values():
                orderitem = OrderItem(
                    order = order,
                    menuitem_id = item['menuitem_id'],
                    price = item['price'],
                    quantity = item['quantity']
                )
                orderitem.save()

            Cart.objects.all().filter(user=self.request.user).delete()

            result = order_serializer.data.copy()
            result['total'] = total
            
            return Response(order_serializer.data)
        
        def get_total_price(self, user):
            total = 0
            items = Cart.objects.all().filter(user=user).all()
            
            for item in items.values():
                total += item['price']

            return total
        

class SingleOrderView(generics.RetrieveUpdateAPIView):
    queryset = Oreder.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if self.request.user.groups.count() == 0:
            return Response("You can't! You're a noraml user.")
        else:
            return super().update(request, *args, **kwargs)


class GroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        users = User.objects.all().filter(groups__name='Manager')
        items = UserSerializer(users, many=True)
        return Response(items.data)
            
    def create(self, requesst):
        user = get_object_or_404(User, username=requesst.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set_add(user)

        return Response({"Message": "added to the manager group"}, status=status.HTTP_200_OK)
    
    def destroy(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        managers = Group.objects.get(name="Manager")
        managers.user_set.remove(user)

        return Response({"Message": "user got removed from the Manager Group."})
    

class DeliveryCrewViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        users = User.objects.all().filter(groups__name='DeliveryCrew')
        items = UserSerializer(users, many=True)
        return Response(items.data)
    
    def create(self, request):
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name="Manager").exists() == False:
                return Response({"Message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, username=request.data['username'])
        dc = Group.objects.get(name='DeliveryCrew')
        dc.user_set.add(user)

        return Response({"Message": "user added to the DC Group"})
    
    def destory(self, request):
        if self.request.user.is_superuser == False:
            if self.request.user.groups.filter(name="Manager").exists() == False:
                return Response({"Message": "Forbidden"},
                                status=status.HTTP_403_FORBIDDEN)
            
            user = get_object_or_404(User, username=request.data['username'])
            dc = Group.objects.get(name="DeliveryCrew")
            dc.user_set.remove(user)

            return Response({"Message": "user removed from the Delivery Crew Group."},
                            status=status.HTTP_200_OK)
        





######### Adding users to Manager Group ###########
# @api_view(["POST"])
# @permission_classes([IsAdminUser])
# def managers(request):
#     username = request.data["username"]
#     if username:
#         user = get_object_or_404(User, username=username)
#         managers = Group.objects.get(name="Manager")
#         if request.method == "POST":
#             managers.user_set.add(user)
#         elif request.method == "DELETE":
#             managers.user_set.remove(user)
        
#         return Response({"Message": "user added to the manager group"})

#     return Response({"Message": "Error!"},
#                     status=status.HTTP_400_BAD_REQUEST)
