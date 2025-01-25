from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Пользователь"))
    package_name = models.CharField(max_length=50, verbose_name=_("Название пакета"))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Сумма"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    is_successful = models.BooleanField(default=False, verbose_name=_("Успешная оплата"))

    def __str__(self):
        return f"{self.package_name} - {self.user.username}"
