import re
import telebot
from pydub import AudioSegment
import speech_recognition as sr
import forrest_app.bd_scripts as bd


def ogg_download(bot: telebot.TeleBot, message: telebot.types.Message) -> str:
    """ Сохраняет файл OGG и возвращает има файла без пути,
        чтобы дальше при конвертации не узнавать user.chat_id """

    user = bd.user(message.chat.id)
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(f'files/{user.chat_id}.ogg', 'wb') as audio_message:
        audio_message.write(downloaded_file)

    return f'{user.chat_id}'


def ogg_to_wav(filename: str, user) -> str:
    """ Сохраняет OGG как WAV """

    dst = f'files/{user.chat_id}.wav'
    sound = AudioSegment.from_ogg(f'{filename}')
    sound.export(dst, format="wav")

    return f'{user.chat_id}.wav'


def wav_to_wav(filename: str, user) -> str:
    """ Сохраняет MP3 как WAV """

    dst = f'files/{user.chat_id}.wav'
    sound = AudioSegment.from_wav(f'{filename}')
    sound.export(dst, format="wav")

    return f'{user.chat_id}.wav'


def mp3_to_wav(filename: str, user) -> str:
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
                -[['боковая рама', 4358973, 43, 1989, 'брак'], ['боковая рама', 4358973, 43, 1989, 'брак'],
                 ['боковая рама', 4358973, 43, 1989, 'брак'], ['боковая рама', 4358973, 43, 1989, 'брак'],
                  ['боковая рама', 4358973, 43, 1989, 'брак']]"""

    string = text.split("следующий")

    pattern = "деталь\s((\S+\s)+)номер(\s(\d+))\sзавод(\s(\d+))\sгод(\s(\d+))\sкомментарий\s((\S+\s)+)"
    tokens = []
    for i in range(len(string)):
        match = re.fullmatch(pattern, string[i])
        if match:
            tokens.append(string[i])

    for i in range(len(tokens)):
        tokens[i] = tokens[i][:len(tokens[i]) - 1]

    final_tokens = []
    for i in range(len(tokens)):
        s = tokens[i].split(" ")

        detail = s[s.index("деталь") + 1:s.index("номер")]
        detail: str = " ".join(detail)
        number = s[s.index("номер") + 1:s.index("завод")]
        number: int = int("".join(number))
        zavod = s[s.index("завод") + 1:s.index("год")]
        zavod: int = int("".join(zavod))
        year = s[s.index("год") + 1:s.index("комментарий")]
        year: int = int("".join(year))
        comment = s[s.index("комментарий") + 1:]
        comment: str = " ".join(comment)
        final_tokens.append([detail, number, zavod, year, comment])

    print(final_tokens)
    return final_tokens

