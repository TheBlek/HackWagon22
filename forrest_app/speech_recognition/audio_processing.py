import re
import speech_recognition as sr
import os

from pydub import AudioSegment
from ..models import BotUser


def ogg_to_wav(filename: str, user: BotUser) -> str:
    """ Сохраняет OGG как WAV """

    dst = f'files/{user.chat_id}.wav'
    sound = AudioSegment.from_ogg(f'{filename}')
    sound.export(dst, format="wav")

    return f'{user.chat_id}.wav'


def wav_to_wav(filename: str, user: BotUser) -> str:
    """ Сохраняет WAV в нужную директорию """

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
        Удаляет файл по-итогу
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
    os.remove(f'files/{filename}')

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
    text = text.replace(",", " ")
    text = text.replace(" номер номер ", " номер ")
    text = text.replace(" завод завод ", " завод ")
    text = text.replace(" от ", " год ")
    text = text.replace(" вгод ", " год ")
    text = text.replace(" в год ", " год ")
    text = text.replace(" зовут ", " завод ")
    text = text.replace(" заводке ", " завод ")
    text = text.replace(" рампа ", " рама ")
    text = text.replace(" равна ", " рама ")
    text = text.replace(" да-да-да ", " ")
    text = text.replace(" вот-вот ", " ")
    text = text.replace("  ", " ")
    text = text.replace(" в ", " ")
    text = text.replace(" а ", " ")
    text = text.replace("начало записи ", " ")
    text = text.replace(" так ", " ")
    text = text.replace(" вот ", " ")
    text = text.replace(" это ", " ")
    text = text.replace(" ещё ", " ")
    text = text.replace(" там ", " ")
    text = text.replace(" запись ", " ")

    text = text.replace(" одиннадцатый ", " 11 ")
    text = text.replace(" одиннадцатая ", " 11 ")
    text = text.replace(" одиннадцатое ", " 11 ")
    text = text.replace(" одиннадцатые ", " 11 ")

    text = text.replace(" двенадцатый ", " 12 ")
    text = text.replace(" двенадцатая ", " 12 ")
    text = text.replace(" двенадцатое ", " 12 ")
    text = text.replace(" двенадцатые ", " 12 ")

    text = text.replace(" тринадцатый ", " 13 ")
    text = text.replace(" тринадцатая ", " 13 ")
    text = text.replace(" тринадцатое ", " 13 ")
    text = text.replace(" тринадцатые ", " 13 ")

    text = text.replace(" четырендцатый ", " 14 ")
    text = text.replace(" четырендцатая ", " 14 ")
    text = text.replace(" четырендцатое ", " 14 ")
    text = text.replace(" четырендцатые ", " 14 ")

    text = text.replace(" пятнадцатый ", " 15 ")
    text = text.replace(" пятнадцатая ", " 15 ")
    text = text.replace(" пятнадцатое ", " 15 ")
    text = text.replace(" пятнадцатые ", " 15 ")

    text = text.replace(" шестнадцатый ", " 16 ")
    text = text.replace(" шестнадцатая ", " 16 ")
    text = text.replace(" шестнадцатое ", " 16 ")
    text = text.replace(" шестнадцатые ", " 16 ")

    text = text.replace(" семнадцатый ", " 17 ")
    text = text.replace(" семнадцатая ", " 17 ")
    text = text.replace(" семнадцатое ", " 17 ")
    text = text.replace(" семнадцатые ", " 17 ")

    text = text.replace(" восемнадцатый ", " 18 ")
    text = text.replace(" восемнадцатая ", " 18 ")
    text = text.replace(" восемнадцатое ", " 18 ")
    text = text.replace(" восемнадцатые ", " 18 ")

    text = text.replace(" девятнадцатый ", " 19 ")
    text = text.replace(" девятнадцатая ", " 19 ")
    text = text.replace(" девятнадцатое ", " 19 ")
    text = text.replace(" девятнадцатые ", " 19 ")

    text = text.replace(" двадцатый ", " 20 ")
    text = text.replace(" двадцатая ", " 20 ")
    text = text.replace(" двадцатое ", " 20 ")
    text = text.replace(" двадцатые ", " 20 ")

    text = text.replace(" двадцать первый ", " 21 ")
    text = text.replace(" двадцать первая ", " 21 ")
    text = text.replace(" двадцать первое ", " 21 ")
    text = text.replace(" двадцать первые ", " 21 ")

    text = text.replace(" двадцать второй ", " 22 ")
    text = text.replace(" двадцать вторая ", " 22 ")
    text = text.replace(" двадцать второе ", " 22 ")
    text = text.replace(" двадцать вторые ", " 22 ")

    text = text.replace(" первый ", " 1 ")
    text = text.replace(" первая ", " 1 ")
    text = text.replace(" первое ", " 1 ")
    text = text.replace(" первые ", " 1 ")

    text = text.replace(" второй ", " 2 ")
    text = text.replace(" вторая ", " 2 ")
    text = text.replace(" второе ", " 2 ")
    text = text.replace(" вторые ", " 2 ")

    text = text.replace(" третий ", " 3 ")
    text = text.replace(" третья ", " 3 ")
    text = text.replace(" третье ", " 3 ")
    text = text.replace(" третьи ", " 3 ")

    text = text.replace(" четвёртый ", " 4 ")
    text = text.replace(" четвёртая ", " 4 ")
    text = text.replace(" четвёртое ", " 4 ")
    text = text.replace(" четвёртые ", " 4 ")

    text = text.replace(" пятый ", " 5 ")
    text = text.replace(" пятая ", " 5 ")
    text = text.replace(" пятое ", " 5 ")
    text = text.replace(" пятые ", " 5 ")

    text = text.replace(" шестой ", " 6 ")
    text = text.replace(" шестая ", " 6 ")
    text = text.replace(" шестое ", " 6 ")
    text = text.replace(" шестые ", " 6 ")

    text = text.replace(" седьмой ", " 7 ")
    text = text.replace(" седьмая ", " 7 ")
    text = text.replace(" седьмое ", " 7 ")
    text = text.replace(" седьмые ", " 7 ")

    text = text.replace(" восьмой ", " 8 ")
    text = text.replace(" восьмая ", " 8 ")
    text = text.replace(" восьмое ", " 8 ")
    text = text.replace(" восьмые ", " 8 ")

    text = text.replace(" девятый ", " 9 ")
    text = text.replace(" девятая ", " 9 ")
    text = text.replace(" девятое ", " 9 ")
    text = text.replace(" девятые ", " 9 ")

    text = text.replace(" десятый ", " 10 ")
    text = text.replace(" десятая ", " 10 ")
    text = text.replace(" десятое ", " 10 ")
    text = text.replace(" десятые ", " 10 ")

    text = text.replace(" следующий ", " ")
    text = text.replace(" следующая ", " ")
    text = text.replace(" следующее ", " ")
    text = text.replace(" следующие ", " ")
    text = text.replace(" следующей ", " ")
    text = text.replace(" следующем ", " ")
    text = text.replace(" следующим ", " ")

    text = text.replace(" есть ", " ")
    text = text.replace(" такой ", " ")
    text = text.replace(" такая ", " ")
    text = text.replace(" такие ", " ")
    text = text.replace(" такое ", " ")
    text = text.replace(" я ", " ")
    text = text.replace(" записывать ", " ")
    text = text.replace(" быково ", " боковая ")
    text = text.replace(" боковой ", " боковая ")
    text = text.replace(" тринадцатый ", " 13 ")
    text = text.replace(" нет ", " ")
    text = text.replace(" раз ", " рама ")
    text = text.replace(" вечером ", " рама ")
    text = text.replace(" трамвай ", " рама ")
    text = text.replace(" равно ", " рама ")
    text = text.replace(" сейчас ", " ")
    text = text.replace(" подойду ", " ")
    text = text.replace(" она ", " ")
    text = text.replace(" он ", " ")
    text = text.replace(" они ", " ")
    text = text.replace(" буква ", " букса ")
    text = text.replace(" равнобоковой ", " рама боковая ")
    text = text.replace(" романовой ", " рама боковая ")
    text = text.replace(" ыково ", " боковая ")

    result = []
    pattern1 = "((([ёа-я]+\s){2})номер\s(((\d+)\s)+)завод\s(((\d+)\s)+)год\s(((\d+)\s)+))"
    everything = re.findall(pattern1, text)
    print(11111111)
    for match in everything:
        splited = match[0].split()
        details = " ".join(splited[:2])

        if splited.index("завод") - splited.index("номер") == 2:
            number = splited[splited.index("номер") + 1]
        else:
            number = "".join(splited[splited.index("номер") + 1:splited.index("завод")])

        if splited.index("год") - splited.index("завод") == 2:
            zavod = splited[splited.index("завод") + 1]
        else:
            zavod = "".join(splited[splited.index("завод") + 1:splited.index("год")])

        year = splited[splited.index("год") + 1]

        if "год" in splited:
            try:
                if len(year) == 1:
                    year = '200' + year
                else:
                    if int(year) < 50:
                        year = '20' + year
                    elif int(year) < 100:
                        year = '19' + year
            except Exception as e:
                pass

        comment = " "

        if "брак" in splited:
            comment = "брак"

        items = [details, number, zavod, year, comment]
        print(items)
        result.append(items)
        text = text.replace(match[0], "")

    pattern2 = "((([ёа-я]+\s){2})номер\s(((\d+)\s)+)год\s(((\d+)\s)+)завод\s(((\d+)\s)+))"
    everything = re.findall(pattern2, text)
    print(22222222)
    for match in everything:
        splited = match[0].split()
        text = text.replace(match[0], "")
        comment = " "
        details = " ".join(splited[:2])

        if splited.index("год") - splited.index("номер") == 2:
            number = splited[splited.index("номер") + 1]
        else:
            number = "".join(splited[splited.index("номер") + 1:splited.index("год")])

        year = "".join(splited[splited.index("год") + 1])

        if "год" in splited:
            try:
                if len(year) == 1:
                    year = '200' + year
                else:
                    if int(year) < 50:
                        year = '20' + year
                    elif int(year) < 100:
                        year = '19' + year
            except Exception as e:
                pass

        if "брак" in splited:
            comment = "брак"

        zavod = "".join(splited[splited.index("завод") + 1:])
        items = [details, number, zavod, year, comment]
        print(items)
        result.append(items)
    pattern3 = "((([ёа-я]+\s){2})номер\s(((\d+)\s)+)год\s(((\d+)\s)+)завод)"
    everything = re.findall(pattern3, text)
    print(33333333)
    for match in everything:
        splited = match[0].split()
        text = text.replace(match[0], "")

        details = " ".join(splited[:2])

        if splited.index("год") - splited.index("номер") == 3:
            number = splited[splited.index("номер") + 1]
            year = splited[splited.index("номер") + 2]
        else:
            number = "".join(splited[splited.index("номер") + 1:splited.index("год") - 1])
            year = splited[splited.index("год") - 1]

        if "год" in splited:
            try:
                if len(year) == 1:
                    year = '200' + year
                else:
                    if int(year) < 50:
                        year = '20' + year
                    elif int(year) < 100:
                        year = '19' + year
            except Exception as e:
                pass

        comment = " "

        if "брак" in splited:
            comment = "брак"

        zavod = "".join(splited[splited.index("год") + 1:splited.index("завод")])
        items = [details, number, zavod, year, comment]
        result.append(items)
        print(items)

    pattern4 = "((([ёа-я]+\s){2})номер\s(((\d+)\s)+)завод\sкитай\sгод\s(((\d+)\s)+))"
    everything = re.findall(pattern4, text)
    for match in everything:
        splited = match[0].split()
        text = text.replace(match[0], "")
        details = " ".join(splited[:2])
        comment = " "
        if splited.index("завод") - splited.index("номер") == 2:
            number = splited[splited.index("номер") + 1]
        else:
            number = "".join(splited[splited.index("номер") + 1:splited.index("завод")])

        year = splited[splited.index("год") + 1]

        if "год" in splited:
            try:
                if len(year) == 1:
                    year = '200' + year
                else:
                    if int(year) < 50:
                        year = '20' + year
                    elif int(year) < 100:
                        year = '19' + year
            except Exception as e:
                pass

        if "брак" in splited:
            comment = "брак"

        items = [details, number, "китай", year, comment]
        print(items)
        result.append(items)

    pattern5 = "((([ёа-я]+\s){1})номер\s(((\d+)\s)+)завод\s(((\d+)\s)+)год\s(((\d+)\s)+))"
    everything = re.findall(pattern5, text)
    print(55555555)
    for match in everything:
        splited = match[0].split()
        details = " ".join(splited[:1])

        if splited.index("завод") - splited.index("номер") == 2:
            number = splited[splited.index("номер") + 1]
        else:
            number = "".join(splited[splited.index("номер") + 1:splited.index("завод")])

        if splited.index("год") - splited.index("завод") == 2:
            factory = splited[splited.index("завод") + 1]
        else:
            factory = "".join(splited[splited.index("завод") + 1:splited.index("год")])

        year = splited[splited.index("год") + 1]

        if "год" in splited:
            try:
                if len(year) == 1:
                    year = '200' + year
                else:
                    if int(year) < 50:
                        year = '20' + year
                    elif int(year) < 100:
                        year = '19' + year
            except Exception as e:
                pass

        comment = " "

        if "брак" in splited:
            comment = "брак"

        items = [details, number, factory, year, comment]
        result.append(items)
        print(items)
        text = text.replace(match[0], "")

    pattern6 = "((([ёа-я]+\s){1})номер\s(((\d+)\s)+)год\s(((\d+)\s)+)завод\s(((\d+)\s)+))"
    everything = re.findall(pattern6, text)
    print(66666666)
    for match in everything:
        splited = match[0].split()
        text = text.replace(match[0], "")
        comment = " "
        details = " ".join(splited[:1])

        if splited.index("год") - splited.index("номер") == 2:
            number = splited[splited.index("номер") + 1]
        else:
            number = "".join(splited[splited.index("номер") + 1:splited.index("год")])

        year = "".join(splited[splited.index("год") + 1])

        if "год" in splited:
            try:
                if len(year) == 1:
                    year = '200' + year
                else:
                    if int(year) < 50:
                        year = '20' + year
                    elif int(year) < 100:
                        year = '19' + year
            except Exception as e:
                pass

        if "брак" in splited:
            comment = "брак"

        zavod = "".join(splited[splited.index("завод") + 1:])
        items = [details, number, zavod, year, comment]
        print(items)
        result.append(items)

    pattern7 = "((([ёа-я]+\s){1})номер\s(((\d+)\s)+)год\s(((\d+)\s)+)завод)"
    everything = re.findall(pattern7, text)
    print(77777777)
    for match in everything:
        splited = match[0].split()
        text = text.replace(match[0], "")

        details = " ".join(splited[:1])

        if splited.index("год") - splited.index("номер") == 3:
            number = splited[splited.index("номер") + 1]
            year = splited[splited.index("номер") + 2]
        else:
            number = "".join(splited[splited.index("номер") + 1:splited.index("год") - 1])
            year = splited[splited.index("год") - 1]

        if "год" in splited:
            try:
                if len(year) == 1:
                    year = '200' + year
                else:
                    if int(year) < 50:
                        year = '20' + year
                    elif int(year) < 100:
                        year = '19' + year
            except Exception as e:
                pass

        comment = " "

        if "брак" in splited:
            comment = "брак"

        zavod = "".join(splited[splited.index("год") + 1:splited.index("завод")])
        items = [details, number, zavod, year, comment]
        print(items)
        result.append(items)

    pattern8 = "((([ёа-я]+\s){1})номер\s(((\d+)\s)+)завод\sкитай\sгод\s(((\d+)\s)+))"
    everything = re.findall(pattern8, text)
    print(88888888)
    for match in everything:
        splited = match[0].split()
        text = text.replace(match[0], "")
        details = " ".join(splited[:2])
        comment = " "
        if splited.index("завод") - splited.index("номер") == 2:
            number = splited[splited.index("номер") + 1]
        else:
            number = "".join(splited[splited.index("номер") + 1:splited.index("завод")])

        year = splited[splited.index("год") + 1]
        if "год" in splited:
            try:
                if len(year) == 1:
                    year = '200' + year
                else:
                    if int(year) < 50:
                        year = '20' + year
                    elif int(year) < 100:
                        year = '19' + year
            except Exception as e:
                pass

        if "брак" in splited:
            comment = "брак"

        items = [details, number, year, "китай", comment]
        print(items)
        result.append(items)

    return result


def normalized_year(year: str) -> str:
    if len(year) == 1:
        year = '200' + year
    else:
        if int(year) < 50:
            year = '20' + year
        elif int(year) < 100:
            year = '19' + year

    return year
