from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class TheatreHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def capacity(self):
        return self.rows * self.seats_in_row


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField("Actor", related_name="plays")
    genres = models.ManyToManyField("Genre", related_name="plays")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE, related_name="performances")
    theatre_hall = models.ForeignKey(
        TheatreHall, on_delete=models.CASCADE, related_name="performances"
    )
    show_time = models.DateTimeField()

    def __str__(self):
        return f"{self.play.title} {self.show_time}"

    class Meta:
        ordering = ["-show_time"]


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, related_name="tickets"
    )

    @staticmethod
    def validate_ticket(row, seat, theatre_hall, error_to_raise):
        for ticket_attr_value, ticket_attr_name, theatre_hall_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(theatre_hall, theatre_hall_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {theatre_hall_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row, self.seat, self.performance.theatre_hall, ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{str(self.performance)} " f"(row: {self.row}, seat: {self.seat})"

    class Meta:
        unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reservations"
    )

    def __str__(self):
        return self.created_at
