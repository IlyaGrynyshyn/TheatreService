from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    PlayViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    ActorViewSet,
    GenreViewSet,
    TicketViewSet, ReservationViewSet
)

router = routers.DefaultRouter()
router.register("actors", ActorViewSet, basename="actors")
router.register("genres", GenreViewSet, basename="genres")
router.register("plays", PlayViewSet, basename="plays")
router.register("theatre_halls", TheatreHallViewSet, basename="theatre_halls")
router.register("performance", PerformanceViewSet, basename="performance")
router.register("tickets", TicketViewSet, basename="tickets")
router.register("reservations", ReservationViewSet, basename="reservations")

urlpatterns = [
    path('', include(router.urls))
]
