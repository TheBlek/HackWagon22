import re
import telebot
from pydub import AudioSegment
import speech_recognition as sr
import forrest_app.bd_scripts as bd


def ogg_download(bot: telebot.TeleBot, message: telebot.types.Message) -> str:
    """ Сохраняет файл ogg и возвращает има файла без пути,
        чтобы дальше при конвертации не узнавать user.chat_id """

    user = bd.user(message.chat.id)
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'files/{user.chat_id}.ogg', 'wb') as audio_message:
        audio_message.write(downloaded_file)

    return f'{user.chat_id}'


def mp3_download(bot: telebot.TeleBot, message: telebot.types.Message) -> str:
    """ Сохраняет файл mp3 и возвращает има файла без пути,
        чтобы дальше при конвертации не узнавать user.chat_id """

    user = bd.user(message.chat.id)
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'files/{user.chat_id}.mp3', 'wb') as audio_message:
        audio_message.write(downloaded_file)

    return f'{user.chat_id}'


def ogg_to_wav(filename: str) -> str:
    """ Сохраняет OGG как WAV """

    dst = f'files/{filename}.wav'
    sound = AudioSegment.from_ogg(f'files/{filename}.ogg')
    sound.export(dst, format="wav")

    return f'files/{filename}.wav'


def mp3_to_wav(filename: str) -> str:
    """ Сохраняет MP3 как WAV """

    dst = f'files/{filename}.wav'
    sound = AudioSegment.from_mp3(f'files/{filename}.mp3')
    sound.export(dst, format="wav")

    return f'files/{filename}.wav'


def audio_processing(filename: str) -> str:
    """ Берётся файл WAV и конвертируется в текст
        Получает на вход:
                -название файла
        Возвращает строку:
                -'апельсины 20 мандарины 13 елочные игрушки 34' """

    rec = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = rec.record(source)
        # recognize (convert from speech to text)
        text = rec.recognize_google(audio_data, language="ru-RU")

    return text


def to_tokens(text: str) -> list:
    """ Берётся list и преобразуется в токены
        Получает на вход:
                -list
        Возвращает лист листов размера 2 вида [[str, int]]:
                -[['апельсины', 20], ['мандарины', 13], ['елочные игрушки', 34]]"""

    tokens = [list(s) for s in re.findall(r"(\D+\s)(\d+)", text)]
    for i in range(1, len(tokens)):
        tokens[i][0] = (tokens[i][0])[1:]
        tokens[i][1] = int(tokens[i][1])

    return tokens
