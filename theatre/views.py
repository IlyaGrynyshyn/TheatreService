from rest_framework import viewsets

from theatre.models import (
    Play,
    TheatreHall,
    Performance,
    Actor,
    Genre,
    Ticket
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
    TicketListSerializer
)


class ActorViewSet(viewsets.ModelViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class PlayViewSet(viewsets.ModelViewSet):
    serializer_class = PlaySerializer
    queryset = Play.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PlayDetailSerializer
        if self.action == "list":
            return PlayListSerializer
        return self.serializer_class


class TheatreHallViewSet(viewsets.ModelViewSet):
    serializer_class = TheatreHallSerializer
    queryset = TheatreHall.objects.all()


class PerformanceViewSet(viewsets.ModelViewSet):
    serializer_class = PerformanceSerializer
    queryset = Performance.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return self.serializer_class

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return self.serializer_class