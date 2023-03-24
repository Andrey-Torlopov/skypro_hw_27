
from django.urls import path

from ads.views import AdDetailView, AdImageView, AdListView

urlpatterns = [
    path("", AdListView.as_view()),
    path("<int:pk>/", AdDetailView.as_view()),
    path('<int:pk>/upload_image/', AdImageView.as_view()),
]
