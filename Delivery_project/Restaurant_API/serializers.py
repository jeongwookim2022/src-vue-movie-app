from rest_framework import serializers

# Models
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuitemSerializer(serializers.ModelSerializer):
    #category = CategorySerializer(read_only=True)
    #category = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title','price','category','featured']

    # A way of showing category's title INSTEAD OF its ID.
    #def to_representation(self, obj):
    #    return {
    #        "category": obj.category.title
    #    }