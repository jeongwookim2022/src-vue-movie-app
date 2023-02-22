from django.shortcuts import render
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework import status

# Models
from .models import *

# Serializers
from .serializers import *

# Create your views here.
class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class MenuitemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuitemSerializer
    filterset_fields = ['price']
    search_fields = ['title']


######### Adding users to Manager Group ###########
@api_view(["POST"])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data["username"]
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method == "POST":
            managers.user_set.add(user)
        elif request.method == "DELETE":
            managers.user_set.remove(user)
        
        return Response({"Message": "user added to the manager group"})

    return Response({"Message": "Error!"},
                    status=status.HTTP_400_BAD_REQUEST)


