from secret_santa_bot.rooms.models import RoomUser, Room
from secret_santa_bot.wishes.models import Wish
from secret_santa_bot.payments.views import PACKAGES


def start(update, context):
    update.message.reply_text(
        "Добро пожаловать к Секретному Санте!!\nКоманды:\n/create - Создать комнату\n/join - Присоединиться к комнате"
    )


def create(update, context):
    user = update.message.from_user
    room_name = context.args[0] if context.args else "My Room"
    room = Room.objects.create(name=room_name, creator=user)
    update.message.reply_text(
        f"Комната создана! Поделись своим кодом с друзьями: {room.code}"
    )


def join(update, context):
    user = update.message.from_user
    code = context.args[0] if context.args else ""
    room = Room.objects.filter(code=code).first()

    if not room:
        update.message.reply_text("Неверный код комнаты.")
        return

    if room.participants.count() >= room.max_users:
        update.message.reply_text("Комната уже полная(")
        return

    if RoomUser.objects.filter(room=room, user=user).exists():
        update.message.reply_text("Вы состоите в этой комнате")
        return

    RoomUser.objects.create(room=room, user=user)
    update.message.reply_text(f"Вы присоединились к комнате: {room.name}!")


def add_wish(update, context):
    user = update.message.from_user
    args = context.args

    if len(args) < 2:
        update.message.reply_text("Используйте: /add_wish [текст до 200 символов]")
        return

    room_code = args[0]
    wish_text = " ".join(args[1:])

    room = Room.objects.filter(code=room_code).first()
    if not room:
        update.message.reply_text("Комната не найдена.")
        return

    if not room.roomuser_set.filter(user=user).exists():
        update.message.reply_text("Вы уже состоите в этой комнате.")
        return

    user_wishes = Wish.objects.filter(user=user, room=room).count()
    if user_wishes >= 2:
        update.message.reply_text("Вы уже достигли лимита по созданным желаниям.")
        return

    Wish.objects.create(user=user, room=room, text=wish_text)
    update.message.reply_text("Желание успешно отправлено.")


def payment_info(update, context):
    """Отправляет информацию о доступных пакетах оплаты."""
    packages_text = "Доступные пакеты:\n"
    for key, package in PACKAGES.items():
        packages_text += f"- {package['name']}: {package['price']} руб. (используйте /pay {key})\n"

    update.message.reply_text(packages_text)


def initiate_payment_telegram(update, context):
    """Инициирует оплату через команду в Telegram."""
    user = update.message.from_user
    args = context.args

    if not args:
        update.message.reply_text("Укажите ключ пакета. Используйте /pay <ключ_пакета>.")
        return

    package_key = args[0]

    if package_key not in PACKAGES:
        update.message.reply_text("Неверный ключ пакета. Используйте /packages для просмотра доступных пакетов.")
        return

    package = PACKAGES[package_key]
    # В реальном проекте здесь будет логика инициации оплаты через платежный сервис
    update.message.reply_text(f"Вы выбрали пакет: {package['name']} за {package['price']} руб. Оплата пока не подключена.")
