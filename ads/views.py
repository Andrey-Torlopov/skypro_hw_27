import json

from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView, DetailView, UpdateView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ads.models import Ad, Category, Selection
from ads.permissions import IsAdSelectionOwner, IsSelectionOwnerPermission
from ads.serializers import (AdCreateSerializer, AdDetailSerializer,
                             AdListSerializer, SelectionCreateSelializer,
                             SelectionSerializer)


def index(request) -> JsonResponse:
    return JsonResponse({"status": "ok"}, status=200)


# * Ad CRUD
class AdListView(ListAPIView):
    queryset = Ad.objects.all()
    default_serializer = AdListSerializer

    serializer_classes = {
        "retrieve": AdDetailSerializer,
        "list": AdListSerializer,
        "create": AdCreateSerializer
    }

    def get(self, request, *args, **kwargs) -> JsonResponse:
        self.queryset = self.queryset.order_by("-price")

        # Фильтр по категориям
        categories_q = None
        if categories := request.GET.getlist('cat', None):
            for item in categories:
                if categories_q is None:
                    categories_q = Q(category__pk__icontains=item)
                else:
                    categories_q |= Q(category__pk__icontains=item)

        if categories_q:
            self.queryset = self.queryset.filter(categories_q)

        # Фильтр по вхождению слова
        if text := request.GET.get('text', None):
            text_q = Q(description__icontains=text)
            text_q |= Q(name__icontains=text)
            self.queryset = self.queryset.filter(text_q)

        # Локация
        if loc_name := request.GET.get('location', None):
            self.queryset = self.queryset.filter(
                Q(author__location__name__icontains=loc_name))

        # Диапазон цен
        if price_from := request.GET.get('price_from', None):
            self.queryset = self.queryset.filter(
                Q(price__gte=price_from))

        if price_to := request.GET.get('price_to', None):
            self.queryset = self.queryset.filter(
                Q(price__lte=price_to))

        return super().get(request, *args, **kwargs)


class AdDetailView(RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdDetailSerializer
    permission_classes = [IsAuthenticated, IsAdSelectionOwner]


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


class AdSelectionView(ModelViewSet):
    queryset = Selection.objects.all()
    default_serializer = SelectionSerializer

    serializer_classes = {
        'create': SelectionCreateSelializer
    }

    default_permission = [AllowAny(), ]
    permissions_list = {
        "create": [IsAuthenticated()],
        "update": [IsAuthenticated(), IsSelectionOwnerPermission()],
        "partial_update": [IsAuthenticated(), IsSelectionOwnerPermission()],
        "destroy": [IsAuthenticated(), IsSelectionOwnerPermission()]
    }

    def get_permissions(self):
        return self.permissions_list.get(self.action, self.default_permission)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)
