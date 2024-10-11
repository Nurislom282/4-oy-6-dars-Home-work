from telebot.types import Message,ReplyKeyboardRemove
from telebot.types import Message, CallbackQuery
import requests
import json

from data import bot
from buttons.default import phone_num
from config import parameters



USER_INFO = {}

def write_to_json(user_info):
    with open('Users_info.json',mode="a",encoding="utf-8") as file:
        json.dump(user_info,file,indent=4)
def validate__name(text):
    if len(text.split()) >= 2 and len(text.split()) <= 4:
        lowercase = "abcdefghijklmnopqrstuvwxyz'"

        name = "".join(text.split()).lower()
        for letter in name:
            if letter not in lowercase:
                return False
        return True
    else:
        return False

def vallidate_phone(phone_number: str):
    if phone_number.startswith("+998") and len(phone_number) == 13:
        if phone_number[1:].isdigit():
            return True
    return False

@bot.message_handler(func=lambda message: message.text == "Ro'yxatdan o'tish📝")
def reg(message: Message):
    from_user_id = message.from_user.id
    USER_INFO[from_user_id] = {}
    msg = bot.send_message(
        chat_id=message.chat.id,
        text="F.I.O kiriting",
        reply_markup=ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(msg, get_full_name)

def get_full_name(message:Message):
    full_name = message.text
    chat_id = message.chat.id
    if validate__name(full_name):
        from_user_id = message.from_user.id
        USER_INFO[from_user_id]["full_name"] = full_name

        msg = bot.send_message(chat_id=chat_id, text="Telefon raqamingizni kiriting.\nExample: +998931232332",
                               reply_markup=phone_num())
        bot.register_next_step_handler(msg, get_phone_number)
    else:
        msg = bot.send_message(
            chat_id=chat_id,
            text="F.I.O t'ogri kiriting",
        )
        bot.register_next_step_handler(msg, get_full_name)

def get_phone_number(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.contact:
        USER_INFO[from_user_id]["phone_number"] = message.contact.phone_number
    else:
        if vallidate_phone(message.text):
            USER_INFO[from_user_id]["phone_number"] = message.text
        else:
            msg = bot.send_message(chat_id=chat_id, text="Telefon raqamingizni to'gri kiriting.\nExample: +998931232332",
                                   reply_markup=phone_num())
            bot.register_next_step_handler(msg, get_full_name)
    del USER_INFO[from_user_id]

@bot.callback_query_handler(func=lambda call: call.data == 'loc')
def reaction_to_ob_havo(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_message(chat_id, "Locatsiyani yuboring")


@bot.message_handler(content_types=['location'])
def loc(message: Message):
    chat_id = message.chat.id
    long = message.location.longitude
    lat = message.location.latitude
    parameters['lat'] = lat
    parameters['lon'] = long

    data = requests.get("https://api.openweathermap.org/data/2.5/weather?", params=parameters).json()
    temp = data["main"]["temp"]
    wind = data["wind"]["speed"]
    text = f"Ob havo ma'lumoti\nTemp: {temp}C\nWind: {wind}"

    write_to_json(USER_INFO)

    bot.send_message(chat_id, text)
