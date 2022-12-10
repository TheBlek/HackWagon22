from time import time
from pydub import AudioSegment

from recognise import recognise


def voice_processing(bot, message) -> str:
    """Получает на вход:
            -инстанс бота
            -сообщение
        Возвращает читаемую строку вида:
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

    # распознание текста из wav файла
    text = recognise(dst)

    return text
