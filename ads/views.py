from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView

from ads.models import Category, Ad


def index(request):
    return JsonResponse({"status": "ok"}, status=200)


class CategoryDetaileView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        item = self.get_object()

        return JsonResponse({
            "id": item.pk,
            "name": item.name
        })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        item = self.get_object()

        return JsonResponse({
            "id": item.pk,
            "name": item.author,
            "price": item.price,
            "description": item.description,
            "address": item.address,
            "is_publish": item.is_published
        }, safe=False)


class CategoryListCreateView(View):
    def get(self, request):
        items = Category.objects.all()
        result = [{"id": item.pk, "name": item.name} for item in items]
        return JsonResponse(result, safe=False)


class AdListCreateView(View):
    def get(self, request):
        items = Ad.objects.all()
        result = [{
            "id": item.pk,
            "name": item.author,
            "price": item.price,
            "description": item.description,
            "address": item.address,
            "is_publish": item.is_published}
            for item in items]
        return JsonResponse(result, safe=False)