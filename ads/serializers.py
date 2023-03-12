from rest_framework import serializers

from ads.models import Ad, Category
from users.serializers import UserListSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    author = UserListSerializer()

    class Meta:
        model = Ad
        fields = '__all__'
