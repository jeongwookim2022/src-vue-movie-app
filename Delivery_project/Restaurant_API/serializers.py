from rest_framework import serializers
from django.contrib.auth.models import User
from decimal import Decimal

# Models
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuitemSerializer(serializers.ModelSerializer):
    #category = CategorySerializer(read_only=True)
    #category = serializers.IntegerField(write_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
        )

    class Meta:
        model = MenuItem
        fields = ['id', 'title','price','category','featured']

    # A way of showing category's title INSTEAD OF its ID.
    #def to_representation(self, obj):
    #    return {
    #        "category": obj.category.title
    #    }

class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        default = serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        attrs['price'] = attrs['quantity']*attrs['unit_price']
        return attrs
    
    class Meta:
        model = Cart
        fields = ['user', 'menuitem', 'unit_price', 'quantity', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

    class meta:
        model = Oreder
        fields = ['id', 'user', 'delivery_crew', 
                  'status', 'date','total',
                  'orderitem']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



