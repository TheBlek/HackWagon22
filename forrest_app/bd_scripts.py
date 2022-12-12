from .models import Items, BotUser


def to_bd(tokens: list, user: BotUser) -> None:
    '''-пробегаемся по каждому набору [ключ, значение]
           -проверка есть ли ключ в бд
           -если да
               -добавляем к значению в бд значение из набора
           -если нет
               -добавляем в бд ключ и значение'''
    values_database = Items.objects.filter(user=user)
    for value_from_voice in tokens:
        tmp_value = Items.objects.filter(user=user, name=value_from_voice[0])
        if len(tmp_value) > 0:
            tmp_value[0].count += value_from_voice[1]
            tmp_value[0].save()
        else:
            Items(user=user,
                  name=value_from_voice[0],
                  count=value_from_voice[1]).save()