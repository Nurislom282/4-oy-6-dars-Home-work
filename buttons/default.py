from telebot.types import ReplyKeyboardMarkup,KeyboardButton


def regiter():
    markap = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Ro'yxatdan o'tish📝")
    markap.add(btn1)
    return markap

def phone_num():
    markap = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("Kotntkni ulashish",request_contact=True)
    markap.add(btn1)
    return markap