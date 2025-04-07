import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.texts import *

from bot import bot
from bot.models import User
from bot.utils import is_active, get_user
from Control.settings import OWNER_ID, CHAT_ID


def startBot(message):
    user_id = message.from_user.id
    user = User.objects.filter(telegram_id=user_id)

    if not user.exists():
        user = User.objects.create(
            telegram_id=user_id,
            access_time_end=datetime.now(),
            username=message.from_user.username,
        )
        user.save()
    else:
        user.first().username = message.from_user.username
        user.first().save()
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton(text = "Готова начать путь к Novoй себе?", callback_data='btn_1')
    markup.add(btn_1)
    bot.send_photo(chat_id=message.chat.id, 
        photo=open(os.path.join(os.path.dirname(__file__),"..", "..", "media", "start.JPEG"), 'rb'),
        caption=start_text,
        reply_markup=markup,
        parse_mode="Markdown"
        )
    #bot.send_message(message.chat.id, start_text, reply_markup=markup)

def forward_check(message):
    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    if message.text == "/start":
        retry_next_step(message.chat.id)
        return
    
    #  Отправка сообщения пользователю о том, что его чек передан админу
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="Написать менеджеру", callback_data='btn_8')
    markup.add(btn)
    bot.send_message(message.chat.id, text_7, reply_markup=markup, parse_mode='Markdown')

    #  Одобрение или отказ админом в доступе
    admin = User.objects.filter(is_admin=True).first()
    ADMIN_PAY = InlineKeyboardMarkup()
    is_extended_ = user.is_extended 
    pay_accept = InlineKeyboardButton(text="Принять", callback_data=f"admin-pay_accept_{message.chat.id}")
    pay_decline = InlineKeyboardButton(text="Отказать", callback_data=f"admin-pay_decline_{message.chat.id}")
    ADMIN_PAY.add(pay_accept, pay_decline)

    #  Перессылка чека
    bot.forward_message(
        chat_id=int(admin.telegram_id),
        message_id=message.id,
        from_chat_id=message.chat.id
    )
    user = get_user(message.chat.id)
    username = user.username
    good = "доступ на 1.5 месяца" if not user.is_paid else "продление на 1 месяц"
    text=f"Новая оплата!\nПользователь @{username} оплатил {good}. Вот чек!" 
    bot.send_message(
        text=text,
        chat_id=int(admin.telegram_id),
        reply_markup=ADMIN_PAY
    )


def admin_check_handler(call):
    _, decision, id_ = call.data.split("_")

    user = get_user(id=id_)
    is_active_ = is_active(user)
    if decision == "accept":
        if not is_active_ and not user.is_extended:
            user.access_time_end = (datetime.now().replace(tzinfo=None) + timedelta(days=45))
        elif is_active_ and not user.is_extended:
            user.access_time_end += timedelta(days=30)
        user.is_paid = True
        if user.is_paid and not user.is_extended:
            user.is_extended = True
        user.save()
        try:
            unban_user(user)
        except Exception as e:
            bot.send_message(
                text=e,
                chat_id=OWNER_ID
            )

        #  Отправляем ссылку пользователю
        link = bot.create_chat_invite_link(chat_id=CHAT_ID, member_limit=1)
        bot.send_message(
            text=f"Чек одобрен!\nВот ссылка на наш чат {link.invite_link}\nЖдем тебя!",
            chat_id=int(user.telegram_id),
            )
    else:
        bot.send_message(
            text="Ваш чек не одобрен! Проверьте все и отправьте еще раз",
            chat_id=int(user.telegram_id),
        )
    bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)
    bot.delete_message(message_id=call.message.id-1, chat_id=call.message.chat.id)


def retry_next_step(id_):
    msg = bot.send_message(id_, "*Попробуйте снова!*\n"+text_6, parse_mode="Markdown")
    bot.register_next_step_handler(msg, forward_check)        



@bot.callback_query_handler(func=lambda call: True)
def callback_r(call):
    user = get_user(call.message.chat.id)
    if call.data == "btn_1":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Программа NOVAя INTENSIVE", callback_data='btn_2')
        markup.add(btn)
        bot.send_message(call.message.chat.id, text_1, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "btn_2":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Что меня ждет?", callback_data='btn_3')
        markup.add(btn)
        bot.send_photo(call.message.chat.id,photo=open(os.path.join(os.path.dirname(__file__),"..", "..",'media','photo_3.JPG'), 'rb'), caption=text_2, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "btn_3":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Что нужно для тренировок?", callback_data='btn_4')
        markup.add(btn)
        """bot.send_photo(chat_id=call.message.chat.id,
                       photo=open(os.path.join(os.path.dirname(__file__),"..", "..",'media','second.JPG'), 'rb'),
                       caption=text_3,
                       reply_markup=markup,
                       parse_mode="Markdown"
                       )"""
        bot.send_message(text=text_3, chat_id=call.message.chat.id, reply_markup=markup, parse_mode="Markdown")
    elif call.data == "btn_4":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Хочу попасть на интенсив 😌", callback_data="btn_5"))
        bot.send_photo(chat_id=call.message.chat.id, photo=open(os.path.join(os.path.dirname(__file__),"..", "..", 'media', 'photo_4.JPG'), 'rb'),caption=text_4, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "btn_5":
        bot.send_media_group(call.message.chat.id, [
            telebot.types.InputMediaPhoto(open(os.path.join(os.path.dirname(__file__),"..", "..", 'media', 'review_4.PNG'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join(os.path.dirname(__file__),"..", "..", 'media', 'review_1.jpg'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join(os.path.dirname(__file__),"..", "..", 'media', 'review_2.PNG'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join(os.path.dirname(__file__),"..", "..", 'media', 'review_3.PNG'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join(os.path.dirname(__file__),"..", "..", 'media', 'review_5.PNG'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join(os.path.dirname(__file__),"..", "..", 'media', 'review_6.PNG'), 'rb')),
            ]
            )
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Зарегистрироваться на интенсив", callback_data='btn_6')
        markup.add(btn)
        bot.send_message(call.message.chat.id, text_5_1, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "btn_6":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Да, готова", callback_data='btn_7')
        markup.add(btn)
        text=text_5_2
        

        """bot.send_photo(chat_id=call.message.chat.id,
                        photo=open(os.path.join(os.path.dirname(__file__),"..", "..","media", "second_2.JPG"), 'rb'),
                        caption=text,
                        reply_markup=markup,
                        parse_mode="Markdown"
                        )"""
        bot.send_message(call.message.chat.id, text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "btn_7":
        text = ''
        if not is_active(user):
            text = text_6
        if not user.is_extended and is_active(user):
            text= '''
            *Продление доступа на 1 месяц*

            Цена: _990 рублей_

            *Готова продолжить тренировки*
            *в NOVAя INTENSIVE?🤸🏻‍♂️*
            '''
        else:
            admin = User.objects.get(telegram_id=call.message.chat.id).username
            text= f"Наша программа доступна лишь на 2.5 месяца. Вы уже обладаете полным доступом!\nЕсли есть вопросы, наш менеджер @{admin} поможет вам и ответит на ваши вопросы"
            bot.send_message(call.message.chat.id,text)
            return
        bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)

        msg = bot.send_message(call.message.chat.id, text_6, parse_mode="Markdown")
        bot.register_next_step_handler(msg, forward_check)        

    elif call.data == "btn_8":
        admin = User.objects.get(telegram_id=call.message.chat.id).username
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Вернуться к оплате", callback_data='btn_6')
        markup.add(btn)
        bot.send_message(call.message.chat.id, f'Наш менеджер @{admin} поможет вам и ответит на ваши вопросы', reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("btn-link"):
        _, id_ = call.data.split("_")
        link = bot.create_chat_invite_link(chat_id=CHAT_ID, member_limit=1)
        bot.send_message(id_, f'Вот ссылка на наш чат {link}\nЖдем тебя!', parse_mode="Markdown")

    elif call.data.startswith("admin-pay"):
        admin_check_handler(call)
def unban_user(user):
    bot.unban_chat_member(chat_id=CHAT_ID, user_id=user.telegram_id)

