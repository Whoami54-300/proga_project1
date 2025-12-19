import os
import telebot

import db


HELP_TEXT = (
    "ToDoList бот.\n\n"
    "Команды:\n"
    "/add <текст> — добавить задачу\n"
    "/list — показать список\n"
    "/delete <id> — удалить задачу по id\n"
    "/edit <id> <новый текст> — изменить задачу по id\n\n"
    "Примеры:\n"
    "/add купить молоко\n"
    "/delete 3\n"
    "/edit 2 купить молоко и хлеб"
)


TOKEN = "7861777768:AAFCX0hBOTCZtuDAqRiySmK4UJEbYSHpk3Y"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def start_help(message):
    db.init_db()
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!\n\n{HELP_TEXT}")


@bot.message_handler(commands=["add"])
def add_task(message):
    db.init_db()
    user_id = message.from_user.id


    text = message.text.split(maxsplit=1)
    if len(text) < 2 or not text[1].strip():
        bot.send_message(message.chat.id, "Использование: /add <текст задачи>")
        return

    try:
        task_id = db.add_task(user_id, text[1])
    except Exception as e:
        bot.send_message(message.chat.id, f"Не смог добавить задачу: {e}")
        return

    bot.send_message(message.chat.id, f"✅ Добавил задачу #{task_id}")


@bot.message_handler(commands=["list"])
def list_tasks(message):
    db.init_db()
    user_id = message.from_user.id

    tasks = db.list_tasks(user_id)
    if not tasks:
        bot.send_message(message.chat.id, "Список пуст. Добавь задачу через /add")
        return

    lines = ["📌 Твои задачи:"]
    for t in tasks:
        lines.append(f"{t['id']}: {t['text']}")
    bot.send_message(message.chat.id, "\n".join(lines))


@bot.message_handler(commands=["delete"])
def delete_task(message):
    db.init_db()
    user_id = message.from_user.id

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        bot.send_message(message.chat.id, "Использование: /delete <id>")
        return

    try:
        task_id = int(parts[1])
    except ValueError:
        bot.send_message(message.chat.id, "id должен быть числом. Пример: /delete 3")
        return

    ok = db.delete_task(user_id, task_id)
    if ok:
        bot.send_message(message.chat.id, f"🗑 Удалил задачу #{task_id}")
    else:
        bot.send_message(message.chat.id, f"Не нашёл задачу #{task_id}")


@bot.message_handler(commands=["edit"])
def edit_task(message):
    db.init_db()
    user_id = message.from_user.id

    
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        bot.send_message(message.chat.id, "Использование: /edit <id> <новый текст>")
        return

    try:
        task_id = int(parts[1])
    except ValueError:
        bot.send_message(message.chat.id, "id должен быть числом. Пример: /edit 2 новый текст")
        return

    new_text = parts[2].strip()
    if not new_text:
        bot.send_message(message.chat.id, "Новый текст не должен быть пустым")
        return

    try:
        ok = db.update_task(user_id, task_id, new_text)
    except Exception as e:
        bot.send_message(message.chat.id, f"Не смог изменить задачу: {e}")
        return

    if ok:
        bot.send_message(message.chat.id, f"✏️ Обновил задачу #{task_id}")
    else:
        bot.send_message(message.chat.id, f"Не нашёл задачу #{task_id}")


if __name__ == "__main__":
    db.init_db()
    bot.infinity_polling()