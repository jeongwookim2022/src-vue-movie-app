from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage

############ Throttling
from rest_framework.throttling import AnonRateThrottle
from rest_framework.decorators import throttle_classes
from rest_framework.throttling import UserRateThrottle
from .throttles import TenCallsPerMinute # Customized throttling

############ Token-based authentication in DRF
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

#### IMPORT your serializer FROM serializer.py
from .serializers import MenuItemSerializer, CategorySerializer

################# Class based views #################
from rest_framework import viewsets
from .models import MenuItem
from .serializers import MenuItemSerializer  

# class MenuItemsViewSet(viewsets.ModelViewSet):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#     ordering_fields = ['price','inventory'] # Sorting by the price & inventory
#     search_fields = ['title', 'category__title'] # As the category is set as a related field in MenuItemSerializer,
#                                                  # it works to search Items by a category's title by adding "category__title".

###################### Generics ######################
# It's much easier and more simple.
from rest_framework import generics

class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title', 'category__id']

#####################################################

# @api_view(["GET", "POST"])
# def menu_items(request):
#     # items = MenuItem.objects.all()
    
#     # when converting a model object to String
#     # you need to load the related Model with SQL code 
#     # - this is for the Foreign Key to store it in cache.
#     if request.method == "GET":
#         items = MenuItem.objects.select_related('category').all()
#         #### Filtering & Searching using the query params in GET METHOD
#         category_name = request.query_params.get('category')
#         to_price = request.query_params.get('to_price')
#         search = request.query_params.get('search')
#         if category_name:
#             items = items.filter(category__title=category_name)
#         if to_price:
#             items = items.filter(price__lte=to_price) # lte: conditional operator or fields lookup
#         if search:
#             items = items.filter(title__contains=search)
#         ####
#         #### Ordering & Sorting
#         ordering = request.query_params.get('ordering')
#         if ordering:
#             ordering_fields = ordering.split(",")
#             items = items.order_by(*ordering_fields)
#         ####
#         #### Pagination(perpage & page)
#         perpage = request.query_params.get('perpage', default=2)
#         page = request.query_params.get('page', default=1)
        
#         paginator = Paginator(items, per_page=perpage)
#         try:
#             items = paginator.page(number=page)
#         except EmptyPage: # when a client requests a not existing page
#             items = []    
#         ####    
#         serialized_item = MenuItemSerializer(items, many=True) # "many=Ture": essential when converting a list to JSON
#         return Response(serialized_item.data)
#     elif request.method == "POST":
#         serialized_item = MenuItemSerializer(data=request.data) # to deserialize the request data, you have to pass it to Serializer
#         serialized_item.is_valid(raise_exception=True) # the request data must include every essetial field data. Raise an exception if any of them is missing
#         serialized_item.save() # save the record in DB
#         return Response(serialized_item.data, status=status.HTTP_201_CREATED)

# @api_view()
# def single_item(request, id):
#     #item = MenuItem.objects.get(pk=id)
#     item = get_object_or_404(MenuItem, pk=id) 
#     serialized_item = MenuItemSerializer(item) # No need to add "many=Ture" when it's a single item
#     return Response(serialized_item.data)

##################Token_based_authentication###############
@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "Some secret message"})

##############Authorization using Token in http post request's header#######
@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        return Response({"message":"Only Managers should see this"})
    else:
        return Response({"Message":"You are not authorized"}, 403)
    
###################Throttling for two kinds users; one who got a token & Second who doesn't######
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "successful"})


# @throttle_classes([UserRateThrottle]) # Using the built in Package class
@api_view()
@throttle_classes([TenCallsPerMinute]) # Customized Throttling for an endpoint
def throttle_check_auth(request):
    return Response({"message": "Message for the logged in users only."})

