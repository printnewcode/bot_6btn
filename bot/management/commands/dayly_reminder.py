from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from pytz import tzinfo

from bot import bot
from bot.models import User
from bot.utils import is_active


class Command(BaseCommand):
    help = "Remind for user during the day"

    def handle(self, *args, **options):
        users = User.objects.filter(is_paid = True)
        for user in users:
            is_active_ = is_active(user)
            if is_active_:
                access_time = user.access_time_end
                diff = access_time.replace(tzinfo=None) - datetime.now().replace(tzinfo=None)
                if diff.days < timedelta(days=5):
                    bot.send_message(text=f"У вас осталось лишь {diff.days} дней доступа! Для дальнейшего пользования, пожалуйста, продлите его")
                else:
                    return
                return
            return