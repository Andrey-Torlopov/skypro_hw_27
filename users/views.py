import json

from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View
from users.models import Location, User


# * User CRUD
class UserListView(ListView):
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.prefetch_related("location")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_objects = paginator.get_page(page_number)

        items_array = []
        for item in page_objects:
            items_array.append(
                {
                    "id": item.pk,
                    "username": item.username,
                    "first_name": item.first_name,
                    "last_name": item.last_name,
                    "role": item.role,
                    "locations": list(item.location.all().values_list("name", flat=True))
                }
            )

        response = {
            "items": items_array,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


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


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs) -> JsonResponse:
        item = self.get_object()

        return JsonResponse(
            {
                "id": item.pk,
                "username": item.username,
                "first_name": item.first_name,
                "last_name": item.last_name,
                "role": item.role,
                "locations": list(item.location.all().values_list("name", flat=True))
            }
        )


@ method_decorator(csrf_exempt, name="dispatch")
class UserCreateView(CreateView):
    model = User

    fields = ["first_name", "last_name", "username",
              "password", "role", "age", "location"]

    def post(self, request, *args, **kwargs) -> JsonResponse:
        data = json.loads(request.body)

        item = User.objects.create(
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
            password=data["role"]
        )

        for location_name in data["location"]:
            location_object, _ = Location.objects.get_or_create(
                name=location_name
            )

            item.location.add(location_object)

        item.save()

        return JsonResponse({
            "id": item.pk,
            "name": item.username,
            "first_name": item.first_name,
            "last_name": item.last_name,
            "role": item.role,
            "locations": list(item.location.all().values_list("name", flat=True))
        })


@ method_decorator(csrf_exempt, name="dispatch")
class UserUpdateView(UpdateView):
    model = User

    fields = ["first_name", "last_name", "username", "role", "age", "location"]

    def patch(self, request, *args, **kwargs) -> JsonResponse:
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        self.object.username = data["username"]
        self.object.password = data["password"]
        self.object.first_name = data["first_name"]
        self.object.last_name = data["last_name"]
        self.object.age = data["age"]

        for location in data["locations"]:
            location_object, _ = Location.objects.get_or_create(
                name=location
            )
            self.object.location.add(location_object)

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "locations": list(self.object.location.all().values_list("name", flat=True))
        })


@ method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
