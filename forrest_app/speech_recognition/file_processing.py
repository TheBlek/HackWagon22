from pydub import AudioSegment
import math
import telebot
import forrest_app.bd_scripts as bd
from .audio_processing import audio_processing, \
                            mp3_to_wav


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
        with open(f'{user.chat_id}.mp3', 'wb') as audio_message:
            audio_message.write(downloaded_file)
        wav_filename = mp3_to_wav(f'{user.chat_id}.mp3', user)
    elif 'wav' in file_info.file_path:
        with open(f'{user.chat_id}.wav', 'wb') as audio_message:
            audio_message.write(downloaded_file)
        wav_filename = f'{user.chat_id}.wav'

    return wav_filename


def separating_and_processing(filename: str) -> str:
    """ Режет файл на файлы поменьше, для обработки с помощью speech_recognition.Recognizer.recognize_google:
        Получает на вход:
                -имя файла
        Возвращает строку - распознанный текст. """

    split_wav = SplitWavAudioMubin("", filename)
    cnt_files = split_wav.multiple_split(filename, min_per_split=1)
    res = []
    for i in range(cnt_files):
        filename_n = str(i) + f'_{filename}'
        res.append(audio_processing(filename_n))

    return ' '.join(res)


class SplitWavAudioMubin:
    def __init__(self, folder: str, filename: str) -> None:
        self.folder = folder
        self.filename = filename
        self.filepath = folder + filename

        self.audio = AudioSegment.from_wav(self.filepath)

    def get_duration(self) -> int:
        return self.audio.duration_seconds

    def single_split(self, from_min: int, to_min: int, split_filename: str) -> None:
        time_1 = from_min * 120 * 1000
        time_2 = to_min * 120 * 1000
        split_audio = self.audio[time_1:time_2]
        split_audio.export(self.folder + split_filename, format="wav")

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
