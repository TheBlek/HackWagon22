from .models import Items, BotUser


def save_tokens(tokens: list, user: BotUser) -> None:
    '''-пробегаемся по каждому набору [ключ, значение]
           -проверка есть ли ключ в бд
           -если да
               -добавляем к значению в бд значение из набора
           -если нет
               -добавляем в бд ключ и значение'''
    for value_from_voice in tokens:
        tmp_value = Items.objects.filter(user=user, name=value_from_voice[0])
        if len(tmp_value) > 0:
            tmp_value[0].count += int(value_from_voice[1])
            tmp_value[0].save()
        else:
            Items(user=user,
                  name=value_from_voice[0],
                  count=value_from_voice[1]).save()

def user(chat_id: int) -> BotUser:
    return BotUser.objects.get(chat_id = chat_id)

