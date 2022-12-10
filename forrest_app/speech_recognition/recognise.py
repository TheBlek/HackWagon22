from audio_processing import audio_processing
import telebot


def recognise(bot: telebot.TeleBot, message: telebot.types.Message) -> str:  # -> DataFrameExtended
    """ Функция (главная по иерархии внутри обработки voice message),
        которая в итоге даёт преобразует в FrameExtended

        Получает на вход:
                -инстанс бота
                -сообщение
        Возвращает DataFrame вида:
                -*потом скопируем код-пример* """

    # распознание текста из wav файла
    text = audio_processing(bot, message)

    return text
