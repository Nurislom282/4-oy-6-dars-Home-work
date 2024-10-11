from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_button():
    markup = InlineKeyboardMarkup()
    btn2 = InlineKeyboardButton("Lokatsiya", callback_data="loc")
    markup.add(btn2)
    return markup


def cities_buttons(city_names: dict):
    markup = InlineKeyboardMarkup()
    for key, city_name in city_names.items():
        btn = InlineKeyboardButton(city_name, callback_data=key)
        markup.add(btn)
    markup.add(InlineKeyboardButton("Ortga", callback_data="back"))
    return markup