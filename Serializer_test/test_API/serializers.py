from rest_framework import serializers
from .models import *
from decimal import Decimal

# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     inventory = serializers.IntegerField()
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "slug", "title"]


class MenuItemSerializer(serializers.ModelSerializer):
    # creating a new field linked to an exisiting field
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = CategorySerializer(read_only=True) # make it "READ_ONLY" cause it only needs to be displayed via GET_CALL.
    category_id = serializers.IntegerField(write_only=True) # I want to save a MENU with a diff category_id
                                                            # Don't want to show category_ID to GET_REQUEST.
    class Meta:
        model = MenuItem
        # fields = ['id', 'title', 'price', 'inventory']
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id'] # Category is set as a related field
        
    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
    