from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ads.models import Ad, Category, Selection
from users.models import User, UserRole
from users.serializers import UserListSerializer


def check_created_published_flag(value: bool) -> None:
    if value:
        raise ValidationError(f"{value} can't be True.")


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


class AdCreateSerializer(serializers.ModelSerializer):
    is_publish = serializers.BooleanField(validators=[check_created_published_flag], default=False)

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
            return ValidationError("Нет доступа")

        return super().create(validated_data)
