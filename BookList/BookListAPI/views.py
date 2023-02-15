from django.shortcuts import render

#####
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from rest_framework.views import APIView

# Create your views here.
@api_view(['GET', 'POST'])
def books(request):
    return Response('List of the books',
                    status=status.HTTP_200_OK)

# 2
class BookList(APIView):
    def get(self, request):
        author = request.GET.get('author')
        if author:
            return Response({"Message":"List of the books by " + author},
                        status=status.HTTP_200_OK)

        return Response({"Message": "List of the books"},
                        status=status.HTTP_201_CREATED)

    def post(self, request):
        return Response({"Title":request.data.get('title')},
                        status=status.HTTP_201_CREATED)
    

class Book(APIView):
    def get(self, request, pk):
        return Response({"Message":"Single book with its id " + str(pk)},
                        status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        return Response({"Title": request.data.get("title")},
                        status=status.HTTP_200_OK)
