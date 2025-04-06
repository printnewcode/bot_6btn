from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from pytz import tzinfo

from bot import bot
from bot.models import User


class Command(BaseCommand):
    help = "Remind for user during the day"

    def handle(self, *args, **options):
        users = User.objects.filter(is_paid = True)
        for user in users:
            is_active = access_time.is_active(user)
            if is_active:
                access_time = user.access_time_end
                diff = access_time.replace(tzinfo=None) - datetime.now().replace(tzinfo=None)
                if int(diff.days) < 5:
                    bot.send_message(text=f"У вас осталось лишь {diff.days} дней доступа! Для дальнейшего пользования, пожалуйста, продлите его")
                else:
                    return
                return
            return