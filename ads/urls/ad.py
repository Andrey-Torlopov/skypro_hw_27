
from django.urls import path

from ads.views import AdDetailView, AdImageView, AdViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register('', AdViewSet)


urlpatterns = [
    path("<int:pk>/", AdDetailView.as_view()),
    path('<int:pk>/upload_image/', AdImageView.as_view()),
]

urlpatterns += router.urls
