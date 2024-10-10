from telebot.types import Message

from data import bot
from buttons.default import regiter

@bot.message_handler(commands=["start"])
def raction_sart(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f"<b>Assalomu alaykum{message.from_user.full_name} obhavo haqida malumotga hush kelibsiz!</b>",
                     parse_mode="html",reply_markup=regiter())