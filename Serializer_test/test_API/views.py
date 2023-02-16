from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.shortcuts import get_object_or_404

# IMPORT your serializer FROM serializer.py
from .serializers import MenuItemSerializer

@api_view()
def menu_items(request):
    items = MenuItem.objects.all()
    serialized_item = MenuItemSerializer(items, many=True) # "many=Ture": essential when converting a list to JSON
    
    return Response(serialized_item.data)

@api_view()
def single_item(request, id):
    #item = MenuItem.objects.get(pk=id)
    item = get_object_or_404(MenuItem, pk=id) 
    serialized_item = MenuItemSerializer(item) # No need to add "many=Ture" when it's a single item
    return Response(serialized_item.data)
