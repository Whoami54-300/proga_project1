import telebot
from telebot import types
# from aiogram import types, executor
# import sheduler
# import dp


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
    # bot.send_message(message.chat.id, "Напиши задачу. Если надо будет удалить, то пиши '-'")

# @dp.message_handler(lambda message: message.text.startswith('-'))
# async def del_task(message: types.Message):
#     """Удаляет одну задачу по её идентификатору (id)"""
#     row_id = int(message.text[1:])
#     sheduler.delete_task(row_id)
#     answer_message = "Задача успешно удалена."
#     await message.answer(answer_message)

# @dp.message_handler()
# async def add_task(message: types.Message):
#     """Добавляет задачу в планировщик"""
#     if not message.text.startswith("/"):
#         chat_id = message.chat.id
#         await sheduler.add_task(message.text, chat_id)

# if __name__ == "__main__":
#     executor.start_polling(dp, skip_updates=True)

bot.polling(none_stop=True)