from functools import partial
import re
import telebot
import forrest_app.bd_scripts as bd

from settings import BOT_TOKEN, BotStates
from .models import BotUser, Items, ItemsForConfirmation
from .speech_recognition.file_processing import file_processing
from .speech_recognition.audio_processing import audio_processing, \
                                                    to_tokens, \
                                                    ogg_download, \
                                                    ogg_to_wav, \
                                                    mp3_download, \
                                                    mp3_to_wav, \
                                                    wav_download


bot: telebot.TeleBot = telebot.TeleBot(BOT_TOKEN)


def in_state(state: BotStates) -> partial:
    def check(state: BotStates, message: telebot.types.Message) -> bool:
        user = BotUser.objects.get(chat_id=message.chat.id)
        return user.state == state.value
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


@bot.message_handler(content_types=['text'], func=in_state(BotStates.REGISTRATION))
def fill_full_name(message: telebot.types.Message) -> None:
    full_name_pattern = re.compile(r"\w+ \w+")
    if full_name_pattern.fullmatch(message.text):
        user = bd.user(message.chat.id)
        user.full_name = message.text
        user.state = BotStates.MAIN_MENU.value
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


@bot.message_handler(commands=['record'], func=in_state(BotStates.MAIN_MENU))
def start_recording(message: telebot.types.Message) -> None:
    # to_do: move to bd_scripts
    user = bd.user(message.chat.id)
    for item in Items.objects.filter(user=user):
        item.delete()
    user.state = BotStates.RECORDING.value
    user.save()

    bot.send_message(
        message.chat.id,
        '''
        Новая запись начата.
        Чтобы добавить предметы отправте голосовое сообщение.
        Чтобы завершить записывание отправьте /finish.
        '''
    )


@bot.message_handler(content_types=['voice'], func=in_state(BotStates.RECORDING))
def process_audio(message: telebot.types.Message) -> None:
    user = bd.user(message.chat.id)

    # так как это голосовое, то скачиваем ogg и конвертируем в wav
    ogg_filename = ogg_download(bot, message)
    wav_filename = ogg_to_wav(ogg_filename)
    text = audio_processing(wav_filename)
    items = to_tokens(text)

    if len(ItemsForConfirmation.objects.filter(user=user)) != 0:
        ItemsForConfirmation.objects.get(user=user).delete()

    for_confirmation = ItemsForConfirmation(user=user, items=items)
    for_confirmation.save()

    bot.send_message(
        message.chat.id,
        f'''
        Вы перечислили:
        {', '.join(map(str, items))}
        Всё правильно?(да/нет)
        '''
    )
    user.state = BotStates.CONFIRMATION.value
    user.save()


@bot.message_handler(content_types=['audio'], func=in_state(BotStates.RECORDING))
def process_file(message: telebot.types.Message) -> None:
    user = bd.user(message.chat.id)

    print('обрабатываю')
    #mp3_filename = mp3_download(bot, message)
    wav_filename = wav_download(bot, message)
    text = file_processing(wav_filename)
    items = to_tokens(text)

    if len(ItemsForConfirmation.objects.filter(user=user)) != 0:
        ItemsForConfirmation.objects.get(user=user).delete()

    for_confirmation = ItemsForConfirmation(user=user, items=items)
    for_confirmation.save()

    bot.send_message(
        message.chat.id,
        f'''
        Вы перечислили:
        {', '.join(map(str, items))}
        Всё правильно?(да/нет)
        '''
    )
    user.state = BotStates.CONFIRMATION.value
    user.save()


@bot.message_handler(content_types=['text'], func=in_state(BotStates.CONFIRMATION))
def confirm_items(message: telebot.types.Message) -> None:
    user = bd.user(message.chat.id)
    if not message.text.lower() in ['да', 'нет']:
        bot.send_message(
            user.chat_id,
            "Я вас не понял, попробуйте снова"
        )
        return

    items = ItemsForConfirmation.objects.get(user=user)
    reply = '''
            Хорошо, не будем их записывать, попробуйте снова.
            Вы можете завершить записывание, написав /finish
            '''
    if message.text.lower() == 'да':
        bd.save_tokens(items.items, user)

        reply = '''
            Отлично, я записал это в таблицу.
            Вы можете завершить записывание, написав /finish '''
    bot.send_message(
        user.chat_id,
        reply
    )

    items.delete()
    user.state = BotStates.RECORDING.value
    user.save()


@bot.message_handler(commands=['check'], func=in_state(BotStates.RECORDING))
def check_database(message: telebot.types.Message) -> None:
    user = bd.user(message.chat.id)
    items = Items.objects.filter(user=user)
    bot.send_message(
        message.chat.id,
        f'''
        Ваша таблица предметов на данный момент:
        {', '.join(map(str, items))}
        '''
    )
    user.save()


@bot.message_handler(commands=['finish'], func=in_state(BotStates.RECORDING))
def finish_recording(message: telebot.types.Message) -> None:
    user = bd.user(message.chat.id)
    items = Items.objects.filter(user=user)
    bot.send_message(
        message.chat.id,
        f'''
        Ваша таблица предметов:
        {', '.join(map(str, items))}
        '''
    )

    frames = bd.to_dataframe(list(items))
    xlsx_file = bd.dataframe_to_excel(frames, str(user.chat_id))
    bot.send_document(message.chat.id, open(xlsx_file, 'rb'))
    user.state = BotStates.MAIN_MENU.value
    user.save()


@bot.message_handler(commands=['help'])
def help_message(message: telebot.types.Message) -> None:
    bot.send_message(
        message.chat.id,
        ''' /record - Начать запись новой таблицы учёта\n/check - Текущее содержимое таблицы учёта '''
    )


@bot.message_handler(commands=['state'])
def print_state(message: telebot.types.Message) -> None:
    user = bd.user(message.chat.id)
    bot.send_message(user.chat_id, "You are in " + BotStates(user.state).name)


@bot.message_handler()
def invalid_message(message: telebot.types.Message) -> None:
    bot.send_message(
        message.chat.id,
        "Простите, я вас не понял. Вы можете посмотреть мои возможности в /help"
    )
