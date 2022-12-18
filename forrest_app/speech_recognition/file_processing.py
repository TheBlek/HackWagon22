import math
import threading
import telebot
import forrest_app.bd_scripts as bd
from pydub import AudioSegment
from .audio_processing import audio_processing, \
                            mp3_to_wav

RES_1: list = []
RES_2: list = []
RES_3: list = []
RES_4: list = []


def recognise_with_threads1(filename: str, begin: int, end: int) -> None:
    global RES_1
    RES_1 = []
    for i in range(begin, end):
        filename_n = str(i) + f'_{filename}'
        RES_1.append(audio_processing(filename_n))


def recognise_with_threads2(filename: str, begin: int, end: int) -> None:
    global RES_2
    RES_2 = []
    for i in range(begin, end):
        filename_n = str(i) + f'_{filename}'
        RES_2.append(audio_processing(filename_n))


def recognise_with_threads3(filename: str, begin: int, end: int) -> None:
    global RES_3
    RES_3 = []
    for i in range(begin, end):
        filename_n = str(i) + f'_{filename}'
        RES_3.append(audio_processing(filename_n))


def recognise_with_threads4(filename: str, begin: int, end: int) -> None:
    global RES_4
    RES_4 = []
    for i in range(begin, end):
        filename_n = str(i) + f'_{filename}'
        RES_4.append(audio_processing(filename_n))


def file_download(bot: telebot.TeleBot, message: telebot.types.Message) -> str:
    """ Помещает файл в нужную нам директорию,
        преобразует в WAV в зависимости от первоначального расширения.
        Получает на вход:
                -инстанс бота
                -сообщение
        Возвращает строку-название файла без пути (но лежит в files/), например
                - 296976920.wav """

    user = bd.user(message.chat.id)
    file_info = bot.get_file(message.audio.file_id)
    wav_filename = ""
    downloaded_file = bot.download_file(file_info.file_path)
    if 'mp3' in file_info.file_path:
        with open(f'files/{user.chat_id}.mp3', 'wb') as audio_message:
            audio_message.write(downloaded_file)
        wav_filename = mp3_to_wav(f'{user.chat_id}.wav', user)
    elif 'wav' in file_info.file_path:
        with open(f'files/{user.chat_id}.wav', 'wb') as audio_message:
            audio_message.write(downloaded_file)
        wav_filename = f'{user.chat_id}.wav'
    return wav_filename


def separating_and_processing(filename: str) -> str:
    """ Режет файл на файлы поменьше, для обработки с помощью speech_recognition.Recognizer.recognize_google:
        Получает на вход:
                -имя файла
        Возвращает строку - распознанный текст. """

    res = []
    split_wav = SplitWavAudioMubin('files', filename)
    cnt_files = split_wav.multiple_split(filename, min_per_split=1)
    threads = []
    thread_1 = threading.Thread(target=recognise_with_threads1, args=(filename, 0, cnt_files//4))
    threads.append(thread_1)
    thread_1.start()
    thread_2 = threading.Thread(target=recognise_with_threads2, args=(filename, cnt_files//4, cnt_files//2))
    threads.append(thread_2)
    thread_2.start()
    thread_3 = threading.Thread(target=recognise_with_threads3, args=(filename, cnt_files//2, 3*(cnt_files//4)))
    threads.append(thread_3)
    thread_3.start()
    thread_4 = threading.Thread(target=recognise_with_threads4, args=(filename, 3*(cnt_files//4), cnt_files))
    threads.append(thread_4)
    thread_4.start()

    global RES_1, RES_2, RES_3, RES_4

    for thr in threads:
        thr.join()

    for elem in RES_1:
        res.append(elem)
    for elem in RES_2:
        res.append(elem)
    for elem in RES_3:
        res.append(elem)
    for elem in RES_4:
        res.append(elem)

    print(' '.join(res))
    return ' '.join(res)


class SplitWavAudioMubin:
    def __init__(self, folder: str, filename: str) -> None:
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '/' + filename

        self.audio = AudioSegment.from_wav(self.filepath)

    def get_duration(self) -> int:
        return self.audio.duration_seconds

    def single_split(self, from_min: int, to_min: int, split_filename: str) -> None:
        time_1 = from_min * 120 * 1000
        time_2 = to_min * 120 * 1000
        split_audio = self.audio[time_1:time_2]
        split_audio.export(self.folder + '/' + split_filename, format="wav")

    def multiple_split(self, filename: str, min_per_split: int) -> int:
        """ Режет аудио:
            Получает на вход:
                    -имя файла
                    -по сколько минут разделять
            Возвращает int - общая длительность (чтобы потом понимать сколько файлов у нас получилось). """

        total_mins = math.ceil(self.get_duration() / 120)
        for i in range(0, total_mins, min_per_split):
            split_fn = str(i) + '_' + f'{filename}'
            self.single_split(i, i + min_per_split, split_fn)
            print(str(i) + ' Done')
            if i == total_mins - min_per_split:
                print('All splited successfully')

        return total_mins
