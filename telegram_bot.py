import telebot
from telebot import types


bot = telebot.TeleBot("7861777768:AAFCX0hBOTCZtuDAqRiySmK4UJEbYSHpk3Y")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} !")
    keyboard = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton(text="Да", callback_data="productive_yes")
    btn_no = types.InlineKeyboardButton(text="Нет", callback_data="productive_no")
    keyboard.add(btn_yes, btn_no)
    bot.send_message(message.chat.id, "Вы продуктивный?!", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "productive_yes":
        bot.send_message(call.message.chat.id, "Это ооочень хорошо)")
    elif call.data == "productive_no":
        bot.send_message(call.message.chat.id, "ПОШЕЛ ОТ СЮДА!")
    bot.answer_callback_query(call.id)



bot.polling(none_stop=True)