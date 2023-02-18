from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework import status

# IMPORT your serializer FROM serializer.py
from .serializers import MenuItemSerializer

@api_view(["GET", "POST"])
def menu_items(request):
    # items = MenuItem.objects.all()
    
    # when converting a model object to String
    # you need to load the related Model with SQL code 
    # - this is for the Foreign Key to store it in cache.
    if request.method == "GET":
        items = MenuItem.objects.select_related('category').all()
        #### Filtering & Searching using the query params in GET METHOD
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price) # lte: conditional operator or fields lookup
        if search:
            items = items.filter(title__contains=search)
        ####
        #### Ordering & Sorting
        ordering = request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        ####    
        serialized_item = MenuItemSerializer(items, many=True) # "many=Ture": essential when converting a list to JSON
        return Response(serialized_item.data)
    elif request.method == "POST":
        serialized_item = MenuItemSerializer(data=request.data) # to deserialize the request data, you have to pass it to Serializer
        serialized_item.is_valid(raise_exception=True) # the request data must include every essetial field data. Raise an exception if any of them is missing
        serialized_item.save() # save the record in DB
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
        



@api_view()
def single_item(request, id):
    #item = MenuItem.objects.get(pk=id)
    item = get_object_or_404(MenuItem, pk=id) 
    serialized_item = MenuItemSerializer(item) # No need to add "many=Ture" when it's a single item
    return Response(serialized_item.data)
