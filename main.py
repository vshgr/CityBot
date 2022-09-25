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
METRO = ""
SCHEDULE = ""
DESCRIPTION = ""
TAGS = []
URL = ""
MARK = ""

tags = []


def send_msg(text):
    url = "https://api.telegram.org/bot" + token + "/sendMessage?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url)
    return results.json()


send_msg("Привет! Мы создаём приложение для путешественников, "
         "и ты в этом нам можешь помочь! Расскажи о своих любимых местах в СПБ")


@bot.message_handler(commands=["start"])
def start(message):
    global tags
    tags = ["Культурные пространства",
            "Открытые пространства",
            "Масштабные кинопоказы",
            "Бары",
            "Парки развлечений",
            "Крыши/смотровые площадки",
            "Планетарий",
            "Пикник",
            "Кулинарные шоу/дегустации",
            "Уютные заведения",
            "Ботанические сады",
            "Романтические кинопоказы",
            "Уличное искусство",
            "Андеграундные мероприятия",
            "Необычные дворы",
            "Фитнес туризм",
            "Тур на воде",
            "Тур по воздуху",
            "Поход",
            "Архитектурный тур",
            "Театральное искусство",
            "Художественное искусство",
            "Музыкальное искусство",
            "Арт-пространства",
            "Экологический туризм",
            "Wellness туризм",
            "Прогулки",
            "Шоппинг",
            "Камерные встречи",
            "Завершить"]

    msg = bot.send_message(message.chat.id, "Для начала введи название места", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    global NAME
    NAME = message.text
    msg = bot.send_message(message.chat.id, "Введи адрес места")
    bot.register_next_step_handler(msg, get_adress)


def get_adress(message):
    global ADRESS
    ADRESS = message.text
    msg = bot.send_message(message.chat.id, "Укажи ближайшую станцию метро")
    bot.register_next_step_handler(msg, get_metro)


def get_metro(message):
    global METRO
    METRO = message.text
    msg = bot.send_message(message.chat.id, "Введи часы работы места, если они есть. Если их нет введи '-'")
    bot.register_next_step_handler(msg, get_schedule)


def get_schedule(message):
    global SCHEDULE
    SCHEDULE = message.text
    rmk = types.ReplyKeyboardMarkup()
    for i in tags:
        rmk.add(types.KeyboardButton(i))
    msg = bot.send_message(message.chat.id, "Выбери теги", reply_markup=rmk)
    bot.register_next_step_handler(msg, get_tags)


def get_tags(message):
    rmk = types.ReplyKeyboardMarkup()
    if message.text == "Завершить":
        msg = bot.send_message(message.chat.id, "Спасибо, теперь добавь ссылку с описанием",
                               reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_url)
    else:
        global TAGS
        TAGS.append(message.text)
        tags.remove(message.text)
        for i in tags:
            rmk.add(types.KeyboardButton(i))
        msg = bot.send_message(message.chat.id, "Можешь выбрать больше тегов", reply_markup=rmk)
        bot.register_next_step_handler(msg, get_tags)


def get_url(message):
    global URL
    URL = message.text
    msg = bot.send_message(message.chat.id, "Если вам есть, что добавить от себя об этом месте, введите в строку ниже,"
                                            " иначе введите '-'")
    bot.register_next_step_handler(msg, get_desc)


def get_desc(message):
    global DESCRIPTION
    DESCRIPTION = message.text
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton("1"), types.KeyboardButton("2"),
            types.KeyboardButton("3"), types.KeyboardButton("4"),
            types.KeyboardButton("5"))
    msg = bot.send_message(message.chat.id, "Дайте оценку", reply_markup=rmk)
    bot.register_next_step_handler(msg, get_mark)


def get_mark(message):
    global MARK
    MARK = message.text
    bot.send_message(message.chat.id, "*Ответ записан!*", reply_markup=types.ReplyKeyboardRemove(),
                     parse_mode='markdown')
    row = [NAME, ADRESS, METRO, SCHEDULE, get_string(TAGS), URL, DESCRIPTION, MARK]
    sheets[0].insert_rows(1, number=1, values=row, inherit=False)
    TAGS.clear()
    send_msg("Можешь добавить ещё одно место")
    start(message)


def get_string(tags):
    s = ""
    for i in tags:
        s = s + i + " "
    return s


bot.polling()
