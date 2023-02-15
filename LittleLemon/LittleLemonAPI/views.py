from django.shortcuts import render

from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer

# Create your views here.

# This Class
# 1. Accepts POST request to create new records
# 2. Displays records
class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer # stores&creats records

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.RetrieveDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer