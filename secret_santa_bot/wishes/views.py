from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from secret_santa_bot.rooms.models import Room
from .models import Wish


def create_wish(request):
    if request.method == 'POST':
        room_code = request.POST.get('room_code')
        wish_text = request.POST.get('text')

        room = get_object_or_404(Room, code=room_code)

        if not room.roomuser_set.filter(user=request.user).exists():
            return JsonResponse({"error": "Вы не состоите в комнате."}, status=400)

        user_wishes = Wish.objects.filter(user=request.user, room=room).count()
        if user_wishes >= 2:
            return JsonResponse(
                {"error": "Лимит по желаниям. \nЧто бы увеличить лимит воспользуйтесь командой: /---"},
                status=400
            )

        # Create wish
        Wish.objects.create(user=request.user, room=room, text=wish_text)
        return JsonResponse({"message": "Ваше желание успешно добавлено."}, status=201)
