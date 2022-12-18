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
        Items(user=user,
              detail=value_from_voice[0],
              number=value_from_voice[1],
              zavod=value_from_voice[2],
              year=value_from_voice[3],
              comment=value_from_voice[4]).save()


def to_dataframe(tokens: list) -> pd.DataFrame:
    """ Преобразуем список Item`ов в Pandas.DataFrame """

    data_frame = pd.DataFrame({'наименование': [],
                               'номер': [],
                               'год': [],
                               'завод': [],
                               'комментарий': []})
    for token in tokens:
        new_frame = pd.DataFrame({'наименование': [token.detail],
                                  'номер': [token.number],
                                  'год': [token.year],
                                  'завод': [token.zavod],
                                  'комментарий': [token.comment]})
        data_frame = pd.concat([data_frame, new_frame], ignore_index=True)

    return data_frame


def dataframe_to_excel(data_frame: pd.DataFrame, filename: str) -> str:
    """ Создание csv таблицы и вывод названия с путем для последующей отправки """

    data_frame.to_csv(f'files/{filename}.csv', columns=['наименование', 'номер', 'год', 'завод', 'комментарий'])

    return f'files/{filename}.csv'


def user(chat_id: int) -> BotUser:
    return BotUser.objects.get(chat_id=chat_id)
