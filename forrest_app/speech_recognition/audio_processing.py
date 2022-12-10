import speech_recognition as sr
from time import time
from pydub import AudioSegment
import telebot


def audio_processing(bot: telebot.TeleBot, message: telebot.types.Message) -> str:
    """ Берётся бот, message и выводится текст из конвертированного в wav ogg`а
        Получает на вход:
                -инстанс бота
                -сообщение
        Возвращает строку вида:
                -апельсины 20 мандарины 15 яблоки 3"""

    # принимаем ogg файл
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file1 = f'{message.chat.id}_{int(time())}.ogg'
    with open(file1, 'wb') as new_file:
        new_file.write(downloaded_file)
    src = file1

    # преобразование в wav
    dst = f'{message.chat.id}_{int(time())}.wav'
    sound = AudioSegment.from_ogg(src)
    sound.export(dst, format="wav")

    r = sr.Recognizer()
    with sr.AudioFile(dst) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language="ru-RU")

    return text
