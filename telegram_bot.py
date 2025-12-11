import telebot


bot = telebot.TeleBot("7861777768:AAFCX0hBOTCZtuDAqRiySmK4UJEbYSHpk3Y")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} !")



bot.polling(none_stop=True)