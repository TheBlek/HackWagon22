import re
import telebot
import speech_recognition as sr
import forrest_app.bd_scripts as bd

from pydub import AudioSegment
from ..models import BotUser


def ogg_download(bot: telebot.TeleBot, message: telebot.types.Message) -> str:
    """ Сохраняет файл ogg и возвращает има файла без пути,
        чтобы дальше при конвертации не узнавать user.chat_id """

    user = bd.user(message.chat.id)
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'{user.chat_id}.ogg', 'wb') as audio_message:
        audio_message.write(downloaded_file)

    return f'{user.chat_id}'


def ogg_to_wav(filename: str, user: BotUser) -> str:
    """ Сохраняет OGG как WAV """

    dst = f'{user.chat_id}.wav'
    sound = AudioSegment.from_ogg(f'{filename}')
    sound.export(dst, format="wav")

    return f'{user.chat_id}.wav'


def mp3_to_wav(filename: str, user: BotUser) -> str:
    """ Сохраняет MP3 как WAV """

    dst = f'{user.chat_id}.wav'
    sound = AudioSegment.from_mp3(f'{filename}')
    sound.export(dst, format="wav")

    return f'{user.chat_id}.wav'


def audio_processing(filename: str) -> str:
    """ Берётся файл WAV и конвертируется в текст
        Получает на вход:
                -название файла
        Возвращает строку:
                -'апельсины 20 мандарины 13 елочные игрушки 34' """

    rec = sr.Recognizer()
    with sr.AudioFile(f'{filename}') as source:
        # listen for the data (load audio to memory)
        audio_data = rec.record(source)
        # recognize (convert from speech to text)
        text = rec.recognize_google(audio_data, language="ru-RU")

    return text


def to_tokens(text: str) -> list:
    """ Берётся list и преобразуется в токены
        Получает на вход:
                -list
        Возвращает лист листов размера 2 вида [[str, int, int, int, str]]:
                -[['боковая рама', 4358973, 43, 1989, 'брак'],
                ['боковая рама', 4358973, 43, 1989, 'брак'],
                 ['боковая рама', 4358973, 43, 1989, 'брак'],
                 ['боковая рама', 4358973, 43, 1989, 'брак'],
                 ['боковая рама', 4358973, 43, 1989, 'брак']]"""

    text = text.replace("\n", "")
    text = text.replace("номер номер", "номер")
    text = text.replace("завод завод", "завод")
    text = text.replace("от", "год")
    text = text.replace("зовут", "завод")
    text = text.replace("заводке", "завод")
    token = text.split("следующ")

    for i in range(len(token)):
        if token[i][:2] == "ая":
            token[i] = token[i][3:]
        elif token[i][:2] == "ее":
            token[i] = token[i][3:]
        elif token[i][:2] == "ие":
            token[i] = token[i][3:]
        elif token[i][0] == " ":
            token[i] = token[i][1:]

    pattern1 = "(.+)номер(.+)завод(.+)год(.+)"
    pattern2 = "деталь(.+)номер(.+)завод(.+)год(.+)"
    res = []
    for tok in token:
        r1 = re.findall(pattern1, tok)
        if r1:
            res.append(list(r1[0]))

    print(res)
    return res
