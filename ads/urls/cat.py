
from django.urls import path

from ads.views import CategoryListCreateView, CategoryDetaileView

urlpatterns = [
    path("", CategoryListCreateView.as_view()),
    path("<int:pk>/", CategoryDetaileView.as_view())
]
