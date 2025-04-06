from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from pytz import tzinfo

from bot import bot
from bot.utils import is_active
from bot.models import User
from Control.settings import CHAT_ID


class Command(BaseCommand):
    help = "Deleting user from chat"

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            is_active = is_active(user)
            if not is_active:
                bot.ban_chat_member(chat_id=CHAT_ID, user_id=int(user.telegram_id), revoke_messages=False)
                bot.send_message(
                    chat_id=int(user.telegram_id),
                    text="Ваш доступ к чату закончился. Продлите его, оплатив доступ на 1 месяц",
                )
                user.is_paid = False
                user.save()