from telebot.types import Message,ReplyKeyboardRemove

from data import bot
from buttons.default import phone_num

USER_INFO = {}
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