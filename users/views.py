import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.generic import View
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from users.models import Location, User
from users.serializers import (LocationSerializer, UserCreateSerializer,
                               UserDestroySerializer, UserListSerializer,
                               UserUpdateSerializer)

# * Location


class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


# * User CRUD
class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserAdDetailView(View):

    def get(self, request, *args, **kwargs) -> JsonResponse:
        user_query_set = User.objects.annotate(total_ads=Count(
            'ad', filter=Q(ad__is_published=True)))

        paginator = Paginator(user_query_set, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_objects = paginator.get_page(page_number)

        users = []
        for item in page_objects:
            users.append({
                "id": item.pk,
                "username": item.username,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "role": item.role,
                "locations": list(item.location.all().values_list("name", flat=True)),
                "total_ads": item.total_ads
            })
        return JsonResponse(users, safe=False)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer
