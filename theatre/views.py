from django.db.models import F, Count
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from theatre.permissions import IsAdminOrIfAuthenticatedReadOnly
from theatre.models import (
    Play,
    TheatreHall,
    Performance,
    Actor,
    Genre,
    Ticket,
    Reservation,
)
from theatre.serializers import (
    PlaySerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    ActorSerializer,
    GenreSerializer,
    PlayDetailSerializer,
    PlayListSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    TicketSerializer,
    TicketListSerializer,
    ReservationSerializer,
)


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PlayViewSet(viewsets.ModelViewSet):
    serializer_class = PlaySerializer
    queryset = Play.objects.prefetch_related("genres", "actors")
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayDetailSerializer
        if self.action == "list":
            return PlayListSerializer
        return self.serializer_class


class TheatreHallViewSet(viewsets.ModelViewSet):
    serializer_class = TheatreHallSerializer
    queryset = TheatreHall.objects.all()
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class PerformanceViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceSerializer

    queryset = Performance.objects.select_related("play", "theatre_hall").annotate(
        tickets_available=(
            F("theatre_hall__rows") * F("theatre_hall__seats_in_row") - Count("tickets")
        )
    )
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return self.serializer_class


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("performance", "reservation")
    serializer_class = TicketSerializer
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return self.serializer_class


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("user")
    serializer_class = ReservationSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
