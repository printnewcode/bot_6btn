import os

from dotenv import load_dotenv
import telebot
from telebot import types
from texts import *

load_dotenv()
token = os.getenv('TOKEN')
OWNER_ID = os.getenv('OWNER_ID')  #'ID админа без ковычек'
link_guest = os.getenv('LINK_GUEST')  #'пригласительная ссылка в чат'
manager = os.getenv('MANAGER_ID')  #'username менеджера через @'

bot = telebot.TeleBot(token)
bot.set_my_commands([types.BotCommand(command="/start", description="Начать!"),])

@bot.message_handler(commands=['start'])
def startBot(message):
    markup = types.InlineKeyboardMarkup()
    btn_1 = types.InlineKeyboardButton(text = "Что такое NOVAя INTENSIVE?", callback_data='btn_1')
    markup.add(btn_1)
    bot.send_photo(chat_id=message.chat.id, 
        photo=open(os.path.join('media', 'start.JPEG'), 'rb'),
        caption=start_text,
        reply_markup=markup,
        parse_mode="Markdown"
        )
    #bot.send_message(message.chat.id, start_text, reply_markup=markup)

def forward_check(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="Отправить пригласительную ссылку", callback_data='btn_link')
    markup.add(btn)
    bot.forward_message(chat_id=OWNER_ID, from_chat_id=message.chat.id, message_id=message.message_id,
                        )
    bot.send_message(
        text='Новая оплата!\nНажмите на кнопку ниже чтобы отправить пользователю пригласительную ссылку',
        chat_id=OWNER_ID,
        reply_markup=markup,
    )
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(text="Написать менеджеру", callback_data='btn_8')
    markup.add(btn)
    bot.send_message(message.chat.id, text_7, reply_markup=markup, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_r(call):
    if call.data == "btn_1":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Программа NOVAя INTENSIVE", callback_data='btn_2')
        markup.add(btn)
        bot.send_message(call.message.chat.id, text_1, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "btn_2":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Что нужно для тренировок?", callback_data='btn_3')
        markup.add(btn)
        bot.send_message(call.message.chat.id, text_2, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "btn_3":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Хочу попасть на интенсив", callback_data='btn_4')
        markup.add(btn)
        bot.send_photo(chat_id=call.message.chat.id,
                       photo=open('media/second.JPG', 'rb'),
                       caption=text_3,
                       reply_markup=markup,
                       parse_mode="Markdown"
                       )

    elif call.data == "btn_4":
        bot.send_media_group(call.message.chat.id, [
            telebot.types.InputMediaPhoto(open(os.path.join('media', 'review_1.jpg'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join('media', 'review_2.PNG'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join('media', 'review_3.PNG'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join('media', 'review_4.PNG'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join('media', 'review_5.PNG'), 'rb')),
            telebot.types.InputMediaPhoto(open(os.path.join('media', 'review_6.PNG'), 'rb')),
            ]
            )
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Зарегистрироваться на интенсив", callback_data='btn_5')
        markup.add(btn)
        bot.send_message(call.message.chat.id, text_4, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "btn_5":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Да, готова", callback_data='btn_6')
        markup.add(btn)
        bot.send_photo(chat_id=call.message.chat.id,
                       photo=open('media/second_2.JPG', 'rb'),
                       caption=text_5,
                       reply_markup=markup,
                       parse_mode="Markdown"
                       )

    elif call.data == "btn_6":
        msg = bot.send_message(call.message.chat.id, text_6, parse_mode="Markdown")
        bot.register_next_step_handler(msg, forward_check)        

    elif call.data == "btn_8":
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(text="Вернуться к оплате", callback_data='btn_6')
        markup.add(btn)
        bot.send_message(call.message.chat.id, f'Наш менеджер {manager} поможет вам и ответит на ваши вопросы', reply_markup=markup, parse_mode="Markdown")

    elif call.data == "btn_link":
        bot.send_message(call.message.chat.id, f'Вот ссылка на наш чат {link_guest}\nЖдем тебя!', parse_mode="Markdown")




bot.polling()