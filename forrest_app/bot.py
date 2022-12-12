from functools import partial
import re
import telebot

from settings import BOT_TOKEN, BotStates
from .models import BotUser

bot: telebot.TeleBot = telebot.TeleBot(BOT_TOKEN)


def in_state(state: BotStates) -> bool:
    def check(state: BotStates, message: telebot.types.Message):
        user = BotUser.objects.get(chat_id = message.chat.id)
        return user.state == state

    return partial(check, state)

@bot.message_handler(commands=['start'])
def start_command(message: telebot.types.Message) -> None:
    user = BotUser(
        chat_id = message.chat.id,
        nickname = message.chat.username,
        state = BotStates.REGISTRATION.value,
    )
    if isinstance(message.chat.first_name, str) and \
        isinstance(message.chat.last_name, str):

        user.full_name = message.chat.first_name + " " + message.chat.last_name
        user.state = BotStates.MAIN_MENU.value
        bot.send_message(
            message.chat.id,
            "Здравствуйте! Можете посмотреть функционал в /help"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Здравствуйте! Для завершения регистрации, напишите нам своё полное имя"
        )

    user.save()


@bot.message_handler(content_types=['text'], func = in_state(BotStates.REGISTRATION))
def fill_full_name(message: telebot.types.Message) -> None:
    full_name_pattern = re.compile(r"\w+ \w+")
    if full_name_pattern.fullmatch(message.text):
        user = BotUser.objects.get(chat_id = message.chat.id)
        user.full_name = message.text
        user.state = BotStates.MAIN_MENU
        user.save()

        bot.send_message(
            message.chat.id,
            "Поздравляю с завершением регистрации! Можете посмотреть функционал в /help"
        )
    else:
        bot.send_message(
            message.chat.id,
            "Кажется, вы написали нам не полное имя, попробуйте еще раз"
        )


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message) -> None:
    bot.send_message(
        message.chat.id,
        "/record - Начать запись новой таблицы учёта"
    )


@bot.message_handler(commands=['state'])
def print_state(message: telebot.types.Message) -> None:
    user = BotUser.objects.get(chat_id = message.chat.id)
    bot.send_message(user.chat_id, "You are in " + BotStates(user.state).name)


@bot.message_handler()
def invalid_message(message: telebot.types.Message) -> None:
    bot.send_message(
        message.chat.id,
        "Простите, я вас не понял. Вы можете посмотреть мои возможности в /help"
    )
