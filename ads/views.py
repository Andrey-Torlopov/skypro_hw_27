import json

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

from ads.models import Ad, Category


def index(request) -> JsonResponse:
    return JsonResponse({"status": "ok"}, status=200)


# * Ad CRUD
class AdListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related(
            "author").order_by("-price")

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get("page")
        page_objects = paginator.get_page(page_number)

        items_array = []
        for item in page_objects:
            items_array.append(
                {
                    "id": item.pk,
                    "name": item.author.username,
                    "price": item.price,
                    "description": item.description,
                    "is_publish": item.is_published
                }
            )

        response = {
            "items": items_array,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }
        return JsonResponse(response, safe=False)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs) -> JsonResponse:
        item = self.get_object()

        return JsonResponse({
            "id": item.pk,
            "name": item.author.username,
            "price": item.price,
            "description": item.description,
            "is_publish": item.is_published
        }, safe=False, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad

    fields = ["name", "price", "description",
              "is_publish", "category", "author"]

    def patch(self, request, *args, **kwargs) -> JsonResponse:
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)

        self.object.name = data["name"]
        self.object.price = int(data["price"])
        self.object.description = data["description"]
        self.object.is_publish = data["is_publish"] == "TRUE"

        self.object.save()

        return JsonResponse({
            "id": self.object.pk,
            "name": self.object.name,
            "price": self.object.price,
            "description": self.object.description,
            "is_publish": self.object.is_published
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdImageView(UpdateView):
    model = Ad

    fields = ["image"]

    def post(self, request, *args, **kwargs) -> JsonResponse:
        self.object = self.get_object()
        self.object.logo = request.FILES["image"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author_id": self.object.author.id,
            "author": self.object.author.first_name,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category_id": self.object.category.id,
            "image": self.object.image.url if self.object.image else None
        })

# * Category CRUD


class CategoryListView(View):
    def get(self, request) -> JsonResponse:
        items = Category.objects.all().order_by("name")
        result = [{"id": item.pk, "name": item.name} for item in items]
        return JsonResponse(result, safe=False)


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs) -> JsonResponse:
        item = self.get_object()

        return JsonResponse({
            "id": item.pk,
            "name": item.name
        })


class CategoryUpdateView(UpdateView):
    model = Category

    fields = ["name"]

    def patch(self, request, *args, **kwargs) -> JsonResponse:
        super().post(request, *args, **kwargs)

        data = json.loads(request.body)
        self.object.name = data["name"]
        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs) -> JsonResponse:
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
