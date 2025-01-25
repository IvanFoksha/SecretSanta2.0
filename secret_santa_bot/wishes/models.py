from django.db import models
from django.contrib.auth.models import User
from rooms.models import Room


class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Желание от {self.user.username} в комнату {self.room.name}: {self.text}"
