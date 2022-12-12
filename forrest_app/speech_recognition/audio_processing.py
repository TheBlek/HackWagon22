import speech_recognition as sr
from pydub import AudioSegment
import re


def audio_processing(filename: str) -> list:
    """ Берётся имя файла и выводится текст из конвертированного в wav ogg`а
        Получает на вход:
                -инстанс бота
                -сообщение
        Возвращает лист листов размера 2 вида [[str, int]]:
                -'апельсины 20 мандарины 13 елочные игрушки 34' """

    # преобразование в wav
    dst = f'../files/{filename}.wav'
    sound = AudioSegment.from_ogg(f'../files/{filename}.ogg')
    sound.export(dst, format="wav")

    r = sr.Recognizer()
    with sr.AudioFile(dst) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data, language="ru-RU")

    return text


def to_tokens(text: str) -> list:
    """ Берётся текст и преобразуется в токены
        Получает на вход:
                -текст
        Возвращает лист листов размера 2 вида [[str, int]]:
                -[['апельсины', 20], ['мандарины', 13], ['елочные игрушки', 34]]"""

    tokens = [list(s) for s in re.findall(r"(\D+\s)(\d+)", text)]
    for i in range(1, len(tokens)):
        tokens[i][0] = (tokens[i][0])[1:]
        tokens[i][1] = int(tokens[i][1])

    return tokens
