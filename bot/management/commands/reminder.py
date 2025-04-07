from django.core.management.base import BaseCommand, CommandError
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import tzinfo

from bot import bot
from bot.models import User
from bot.texts import TEXT_REMINDER

markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton(text="Связаться с Анастасией", url="https://t.me/anastasiai"))

class Command(BaseCommand):
    help = "Remind for user during the day"

    def handle(self, *args, **options):
        users = User.objects.filter(is_paid = False)
        for user in users:
            access_time = user.access_time_end
            
            if datetime.now().replace(tzinfo=None) - access_time.replace(tzinfo=None) >= timedelta(hours=1):
                bot.send_message(text=TEXT_REMINDER, chat_id = user.telegram_id, reply_markup=markup, parse_mode="Markdown")
                user.is_reminded = True
                user.save()