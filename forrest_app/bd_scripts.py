import pandas as pd
from .models import Items, BotUser


def save_tokens(tokens: list, user: BotUser) -> None:
    """ Пробегаемся по каждому набору [ключ, значение]
           -проверка есть ли ключ в бд
           -если да
               -добавляем к значению в бд значение из набора
           -если нет
               -добавляем в бд ключ и значение """

    values_database = Items.objects.filter(user=user)
    for value_from_voice in tokens:
        tmp_value = Items.objects.filter(user=user, detail=value_from_voice[0])
        if len(tmp_value) > 0:
            tmp_value[0].number += int(value_from_voice[1])
            tmp_value[0].save()
        else:
            Items(user=user,
                  detail=value_from_voice[0],
                  number=value_from_voice[1],
                  zavod=value_from_voice[2],
                  year=value_from_voice[3])
                  # comment=value_from_voice[4]).save()


def to_dataframe(tokens: list) -> pd.DataFrame:
    """ Преобразуем список Item`ов в Pandas.DataFrame """

    data_frame = pd.DataFrame({'Деталь': [],
                              'Номер детали': [],
                              'Завод': [],
                               'Год': [],
                               'Коментарий': []})
    for token in tokens:
        new_frame = pd.DataFrame({'Деталь': [token.detail],
                                  'Номер детали': [token.number],
                                  'Завод': [token.zavod],
                                  'Год': [token.year],
                                  'Комментарий': [token.comment]})
        data_frame = pd.concat([data_frame, new_frame], ignore_index=True)

    return data_frame


def dataframe_to_excel(data_frame: pd.DataFrame, filename: str) -> str:
    """ Создание xlsx таблицы и вывод названия с путем для последующей отправки """

    data_frame.to_excel(f'files/{filename}.xlsx')

    return f'files/{filename}.xlsx'


def user(chat_id: int) -> BotUser:
    return BotUser.objects.get(chat_id=chat_id)
