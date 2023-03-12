from rest_framework import serializers

from users.models import Location, User


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    # NEW
    location = LocationSerializer(many=True)

    # OLD
    # location = serializers. SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field="name"
    # )

    class Meta:
        model = User
        exclude = ['password']


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    location = serializers.SlugRelatedField(
        many=True,
        required=False,
        queryset=Location.objects.all(),
        slug_field="name"
    )

    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self, raise_exception=False) -> bool:
        self._locations = self.initial_data.pop("location")

        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data) -> User:
        item = User.objects.create(**validated_data)

        for location_name in self._locations:
            location_object, _ = Location.objects.get_or_create(
                name=location_name)
            item.location.add(location_object)

        item.save()

        return item


class UserUpdateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        exclude = ['password']

    def is_valid(self, raise_exception=False) -> bool:
        self._locations = self.initial_data.pop("location")

        return super().is_valid(raise_exception=raise_exception)

    def save(self) -> User:
        user = super().save()

        for location in self._locations:
            location_object, _ = Location.objects.get_or_create(name=location)
            user.location.add(location_object)

        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        field = ["id"]
