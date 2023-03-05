
from ads.views import CategoryDeleteView, CategoryDetailView, CategoryListView, CategoryUpdateView
from django.urls import path

urlpatterns = [
    path("", CategoryListView.as_view()),
    path("<int:pk>/", CategoryDetailView.as_view()),
    path("<int:pk>/update/", CategoryUpdateView.as_view()),
    path("<int:pk>/delete/", CategoryDeleteView.as_view())
]
