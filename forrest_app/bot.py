import datetime
import settings
from .models import *
import telebot
from .keyboards import *
from .models import *
from .bd_scripts import *

bot: telebot.TeleBot = telebot.TeleBot(settings.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message) -> None:
    pass


@bot.message_handler(commands=['today'])
def today_command(message: telebot.types.Message) -> None:
    user: BotUser = BotUser.objects.get(telegram_id=message.chat.id)



@bot.message_handler(content_types=['text'])
def text(message: telebot.types.Message) -> None:
    bot.send_message(message.chat.id, message.text)
