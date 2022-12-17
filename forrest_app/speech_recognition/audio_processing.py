import re
import telebot
import speech_recognition as sr
import forrest_app.bd_scripts as bd

from pydub import AudioSegment
from ..models import BotUser


def ogg_to_wav(filename: str, user: BotUser) -> str:
    """ Сохраняет OGG как WAV """

    dst = f'files/{user.chat_id}.wav'
    sound = AudioSegment.from_ogg(f'{filename}')
    sound.export(dst, format="wav")

    return f'{user.chat_id}.wav'


def wav_to_wav(filename: str, user: BotUser) -> str:
    """ Сохраняет MP3 как WAV """

    dst = f'files/{user.chat_id}.wav'
    sound = AudioSegment.from_wav(f'{filename}')
    sound.export(dst, format="wav")

    return f'{user.chat_id}.wav'


def mp3_to_wav(filename: str, user: BotUser) -> str:
    """ Сохраняет MP3 как WAV """

    dst = f'files/{user.chat_id}.wav'
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
    with sr.AudioFile(f'files/{filename}') as source:
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

    text = text.replace('следующая', 'следующий')
    text = text.replace('следующей', 'следующий')
    text = text.replace('следующих', 'следующий')
    text = text.replace('следующим', 'следующий')
    text = text.replace('следующем', 'следующий')
    string = text.split("следующий")
    pattern = "\s((\S+\s)+)номер(\s(\d+))\sзавод(\s(\d+))\s(год|от)(\s(\d+))\sкомментари(и|й)(\s(\S+)+)"
    tokens = []
    for i in range(len(string)):
        print(string[i].lower())
        match = re.fullmatch(pattern, string[i].lower())
        if match:
            tokens.append(string[i].lower())

    for i in range(len(tokens)):
        tokens[i] = tokens[i][:len(tokens[i]) - 1]
    final_tokens = []
    for i in range(len(tokens)):
        s = tokens[i].split(" ")

        detail_s = s[s.index("деталь") + 1:s.index("номер")]
        detail = " ".join(detail_s)
        number_s = s[s.index("номер") + 1:s.index("завод")]
        number = int("".join(number_s))
        zavod_s = s[s.index("завод") + 1:s.index("год")]
        zavod = int("".join(zavod_s))
        year_s = s[s.index("год") + 1:s.index("комментарий")]
        year = int("".join(year_s))
        comment_s = s[s.index("комментарий") + 1:]
        comment = " ".join(comment_s)
        final_tokens.append([detail, number, zavod, year, comment])

    return final_tokens
