from dataclasses import field

from pkg_resources import require
from rest_framework import serializers

from ads.models import Ad, Category, Selection
from users.models import User, UserRole
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


class AdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSelializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all(), required=False)

    class Meta:
        model = Selection
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get("request")
        if "owner" not in validated_data:
            validated_data["owner"] = request.user
        elif "owner" in validated_data and request.user.role == UserRole.MEMBER and request.user != validated_data['owner']:
            raise PermissionError("Нет доступа")

        return super().create(validated_data)
