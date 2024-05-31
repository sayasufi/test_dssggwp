from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Room(models.Model):
    room_number = models.IntegerField(unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Комната {self.room_number}"


class RoomBooking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    purpose = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def clean(self):
        # Check for booking conflicts
        if RoomBooking.objects.filter(
                room=self.room,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
        ).exclude(pk=self.pk).exists():
            raise ValidationError('Комната уже забронирована на это время.')

    def __str__(self):
        return f"{self.room} с {self.start_time} до {self.end_time} для {self.purpose}"
