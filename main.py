import telebot
from telebot import types
import pygsheets

user_dict = {}
gc = pygsheets.authorize(service_file='credentionals.json')

sheets = gc.open('Места СПБ')
worksheet = sheets[0]

token = "5365557057:AAEE2nGlJvMxYUA7TEmAJ36dH1lHj7eBd0M"
bot = telebot.TeleBot('5365557057:AAEE2nGlJvMxYUA7TEmAJ36dH1lHj7eBd0M')


class User:
    def __init__(self, ident):
        self.ident = ident
        self.NAME = ""
        self.ADRESS = ""
        self.METRO = ""
        self.SCHEDULE = ""
        self.DESCRIPTION = ""
        self.TAGS = []
        self.URL = ""
        self.MARK = ""
        self.tags = []


@bot.message_handler(commands=["start"])
def start(message):
    chat = message.chat.id
    ident = message.from_user.id
    userid = User(ident)
    user_dict[chat] = userid
    msg = bot.send_message(chat, "Для начала введи название места", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    if message.text == "/restart":
        start(message)
    chat = message.chat.id
    name = message.text
    userid = user_dict[chat]
    userid.NAME = name
    userid.tags = ["Культурные пространства",
                   "Открытые пространства",
                   "Кинопоказы",
                   "Клубы & бары",
                   "Парки развлечений",
                   "Уличное искусство",
                   "Необычные дворы",
                   "Крыши / смотровые площадки",
                   "Скейтпарки",
                   "Архитектурный тур",
                   "Театральное искусство",
                   "Музеи и выставки",
                   "Музыкальное искусство",
                   "Арт - пространства",
                   "Тематические встречи",
                   "Прогулки",
                   "Шоппинг",
                   "Уютные заведения",
                   "Рестораны & дегустации",
                   "Зоо пространства",
                   "Завершить"]
    msg = bot.send_message(chat, "Введи адрес места")
    bot.register_next_step_handler(msg, get_adress)


def get_adress(message):
    if message.text == "/restart":
        start(message)
    chat = message.chat.id
    adress = message.text
    userid = user_dict[chat]
    userid.ADRESS = adress
    msg = bot.send_message(chat, "Укажи ближайшую станцию метро")
    bot.register_next_step_handler(msg, get_metro)


def get_metro(message):
    if message.text == "/restart":
        start(message)
    chat = message.chat.id
    metro = message.text
    userid = user_dict[chat]
    userid.METRO = metro
    msg = bot.send_message(chat, "Введи часы работы места, если они есть. Если их нет введи '-'")
    bot.register_next_step_handler(msg, get_schedule)


def get_schedule(message):
    if message.text == "/restart":
        start(message)
    chat = message.chat.id
    schedule = message.text
    userid = user_dict[chat]
    userid.SCHEDULE = schedule
    rmk = types.ReplyKeyboardMarkup()
    for i in userid.tags:
        rmk.add(types.KeyboardButton(i))
    msg = bot.send_message(chat, "Выбери теги", reply_markup=rmk)
    bot.register_next_step_handler(msg, get_tags)


def get_tags(message):
    bot.send_message(message.chat.id, "Добавляем...", reply_markup=types.ReplyKeyboardRemove())
    chat = message.chat.id
    tag = message.text
    userid = user_dict[chat]
    if message.text == "/restart":
        start(message)
        userid.TAGS.clear()
    rmk = types.ReplyKeyboardMarkup()
    if message.text == "Завершить":
        msg = bot.send_message(message.chat.id, "Спасибо, теперь добавь ссылку с описанием",
                               reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_url)
    else:
        userid.TAGS.append(tag)
        for i in userid.tags:
            rmk.add(types.KeyboardButton(i))
        msg = bot.send_message(message.chat.id, "Можешь выбрать больше тегов", reply_markup=rmk)
        bot.register_next_step_handler(msg, get_tags)


def get_url(message):
    chat = message.chat.id
    url = message.text
    userid = user_dict[chat]
    if message.text == "/restart":
        start(message)
        userid.TAGS.clear()
    userid.URL = url
    msg = bot.send_message(chat, "Если вам есть, что добавить от себя об этом месте, введите в строку ниже,"
                                 " иначе введите '-'")
    bot.register_next_step_handler(msg, get_desc)


def get_desc(message):
    chat = message.chat.id
    desc = message.text
    userid = user_dict[chat]
    userid.DESCRIPTION = desc
    if message.text == "/restart":
        start(message)
        userid.TAGS.clear()
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton("1"), types.KeyboardButton("2"),
            types.KeyboardButton("3"), types.KeyboardButton("4"),
            types.KeyboardButton("5"))
    msg = bot.send_message(chat, "Дайте оценку", reply_markup=rmk)
    bot.register_next_step_handler(msg, get_mark)


def get_mark(message):
    chat = message.chat.id
    mark = message.text
    userid = user_dict[chat]
    userid.MARK = mark
    if message.text == "/restart":
        start(message)
        userid.TAGS.clear()
    bot.send_message(message.chat.id, "*Ответ записан!*\n Можешь добавить ещё одно место",
                     reply_markup=types.ReplyKeyboardRemove(),
                     parse_mode='markdown')
    row = [userid.NAME, userid.ADRESS, userid.METRO, userid.SCHEDULE, get_string(userid.TAGS), userid.URL,
           userid.DESCRIPTION, userid.MARK]
    sheets[0].insert_rows(1, number=1, values=row, inherit=False)
    userid.TAGS.clear()
    bot.send_message(chat, "Можешь добавить ещё одно место")
    start(message)


def get_string(tags):
    s = ""
    for i in tags:
        if i == tags[-1]:
            s = s + i
        else:
            s = s + i + "\n"
    return s


while True:
    try:
        bot.polling()
    except:
        continue
