import datetime
import settings
from .keyboards import *
from .models import *
from .bd_scripts import *

bot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message):
    pass


@bot.message_handler(commands=['today'])
def start_command(message):
    pass


@bot.message_handler(content_types=['text'])
def text(message):
    bot.send_message(message.chat.id, message.text)
