import requests
import telebot
from telebot import types
import pygsheets

gc = pygsheets.authorize(service_file='credentionals.json')

sheets = gc.open('Места СПБ')
worksheet = sheets[0]

token = "5365557057:AAEE2nGlJvMxYUA7TEmAJ36dH1lHj7eBd0M"
bot = telebot.TeleBot('5365557057:AAEE2nGlJvMxYUA7TEmAJ36dH1lHj7eBd0M')
chat_id = "838481251"

NAME = ""
ADRESS = ""
DESCRIPTION = ""
TAGS = []

tags_text = []


def send_msg(text):
    url = "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url)
    return results.json()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет, это бот для поиска интересных мест в Санкт-Петербурге. "
                                      "Заранее благодарим тебя за помощь")
    msg = bot.send_message(message.chat.id, "Для начала введи название места")
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    tags_text.append("Крыши")
    tags_text.append("Парки")
    tags_text.append("Выставки")
    tags_text.append("Завершить")
    global NAME
    NAME = message.text
    msg = bot.send_message(message.chat.id, "Введи адрес места")
    bot.register_next_step_handler(msg, get_adress)


def get_adress(message):
    global ADRESS
    ADRESS = message.text
    msg = bot.send_message(message.chat.id, "Введи описание места")
    bot.register_next_step_handler(msg, get_desc)


def get_desc(message):
    global DESCRIPTION
    DESCRIPTION = message.text
    rmk = types.ReplyKeyboardMarkup()
    for i in tags_text:
        rmk.add(types.KeyboardButton(i))
    msg = bot.send_message(message.chat.id, "Выбери теги", reply_markup=rmk)
    bot.register_next_step_handler(msg, get_tags)


def get_tags(message):
    if message.text == "Завершить":
        bot.send_message(message.chat.id, "*Ответ записан!*", reply_markup=types.ReplyKeyboardRemove(),
                         parse_mode='markdown')
        send_msg(f"Ответ:\nНазвание места: {NAME}\nАдрес: {ADRESS}\n"
                 f"Описание места: {DESCRIPTION}\nВведённые теги: {TAGS}")
        row = [NAME, ADRESS, DESCRIPTION, get_string(TAGS)]
        worksheet.insert_rows(1, number=1, values=row, inherit=False)
        bot.send_message(message.chat.id, "*Можешь ввести ещё одно место*", parse_mode='markdown')
        TAGS.clear()
        tags_text.clear()
        start(message)
    else:
        TAGS.append(message.text)
        tags_text.remove(message.text)
        rmk = types.ReplyKeyboardMarkup()
        for i in tags_text:
            rmk.add(types.KeyboardButton(i))
        msg = bot.send_message(message.chat.id, "Можешь добавить больше тегов", reply_markup=rmk)
        bot.register_next_step_handler(msg, get_tags)


def get_string(tags):
    s = ""
    for i in tags:
        s = s + i + " "
    return s


bot.polling()
