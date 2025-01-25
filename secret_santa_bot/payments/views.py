from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Payment
import json

PACKAGES = {
    "single_view": {"name": "Просмотр одного желания", "price": 99},
    "full_access": {"name": "Полный доступ", "price": 799},
}

@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        package_key = data.get("package_key")

        if package_key not in PACKAGES:
            return JsonResponse({"error": "Неверный пакет оплаты."}, status=400)

        package = PACKAGES[package_key]
        payment = Payment.objects.create(
            user=request.user,
            package_name=package["name"],
            amount=package["price"],
        )

        # Здесь можно интегрировать платежный сервис (например, YooKassa, Stripe и т.д.)

        return JsonResponse({
            "message": "Оплата инициирована.",
            "payment_id": payment.id,
            "amount": package["price"],
        }, status=201)

    return JsonResponse({"error": "Неверный метод запроса."}, status=405)
