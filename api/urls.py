from django.urls import include, path
from rest_framework import routers

from subway_kl import api as subway_kl_api

app_name = "api"


router = routers.DefaultRouter()
router.register(r"subway", subway_kl_api.SubwayOutletViewSet, basename="subway")

urlpatterns = [
    path("", include(router.urls)),
]
