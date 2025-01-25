from django.shortcuts import JsonResponce
from django.shortcuts import get_object_or_404
from . import models


def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        max_users = int(request.POST.get('max_users', 5))
        room = models.Room.objects.create(name=name, creator=request.user, max_users=max_users)
        return JsonResponce({'name': room.name, 'code': room.code, 'max_users': room.max_users})


def join_room(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        room = get_object_or_404(models.Room, code=code)

        if models.room.participants.count() >= room.max_users:
            return JsonResponce({"error": "Комната полная"}, status=400)

        if models.RoomUser.objects.filter(room=room, user=request.user).exists():
            return JsonResponce(
                {"error": "Вы уже находитесь в этой комнате"},
                status=400
            )

        models.RoomUser.objects.create(room=room, user=request.user)
        return JsonResponce({
            "message":
            f"Поздравляю! Хо-Хо-Хо, вы присоединились к комнате: {room.name}"
        })
