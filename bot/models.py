from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone

class User(models.Model):
    is_paid = models.BooleanField(
        default = False,
        verbose_name = "Оплата"
    )
    username = models.CharField(
        default="none",
        max_length=100
    )
    is_extended = models.BooleanField(
        default = False,
        verbose_name = "Продлевал ли человек на 1 месяц"
    )
    is_reminded = models.BooleanField(
        default = False,
    )
    is_admin = models.BooleanField(
        default = False,
        null = True,
        blank = True,
        verbose_name = "Админ"
    )
    telegram_id = models.CharField(
        max_length = 50,
        verbose_name = "Телеграм-айди пользователя"
    )
    access_time_end = models.DateTimeField(
        auto_now = False,
        auto_now_add = False,
        verbose_name = "Время конца доступа",
        default = datetime.now(),
    )
    def __str__(self):
        return str(self.telegram_id)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
