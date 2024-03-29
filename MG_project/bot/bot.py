import requests
import json
import telebot
import sys
import config

sys.stdout = sys.stderr

bot: telebot.TeleBot
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['bestset'])
def bestset(message):
    enc = json.encoder.JSONEncoder()
    query_json = enc.encode({})
    req = requests.get(f"http://{config.BACK_ADRESS}/bestset",
                       json=query_json, headers=config.HEADERS)
    course = json.loads(req.content)
    ret = f"Ваш случайный набор в Monkey Grinder готов! Напиток: {course['drink']} , и перекус: {course['dish']}."
    bot.send_message(text=ret, chat_id=message.chat.id)


@bot.message_handler(commands=['start', 'reset'])
def start(message):
    bot.send_message(message.chat.id, "Всё готово. `/bestset` чтобы получить свой случайный набор")


if __name__ == "__main__":
    bot.infinity_polling()
    pass
