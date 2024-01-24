from django.urls import path, include
from rest_framework import routers

from theatre.views import PlayViewSet, TheatreHallViewSet, PerformanceViewSet

router = routers.DefaultRouter()
router.register("plays", PlayViewSet, basename="plays")
router.register("theatre_halls", TheatreHallViewSet, basename="theatre_halls")
router.register("performance", PerformanceViewSet, basename="performance")

urlpatterns = [
    path('', include(router.urls))
]
