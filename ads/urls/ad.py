
from ads.views import AdDetailView, AdImageView, AdListView
from django.urls import path

urlpatterns = [
    path("", AdListView.as_view()),
    path("<int:pk>/", AdDetailView.as_view()),
    path('<int:pk>/upload_image/', AdImageView.as_view()),
]
