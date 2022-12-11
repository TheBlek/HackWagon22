from django.db import models
from settings import BotStates


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(primary_key=True,
                                         verbose_name='ID в телеграм',
                                         null=False,
                                         blank=False
                                         )

    nickname = models.TextField(verbose_name='Никнейм',
                                null=False,
                                blank=False)

    full_name = models.TextField(verbose_name='ФИО',
                                 null=False,
                                 blank=False)

    STATES = [
        (BotStates.REGISTRATION.value, BotStates.REGISTRATION.name),
        (BotState.MAIN_MENU.value, BotStates.MAIN_MENU.name),
        (BotState.RECORDING.value, BotStates.RECORDING.name),
    ]

    state = models.IntegerField(verbose_name='Текущее состояние',
                                choices=STATES,
                                default=BotStates.REGISTRATION.value
                                null=False,
                                black=False)

    objects = models.Manager()

    def __str__(self) -> str:
        return f'#{self.telegram_id} @{self.nickname}'

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


# class Value(models.Model):
#     user = models.ForeignKey(to=BotUser,
#                              on_delete=models.CASCADE)
#     key = models.CharField(max_length=50)
#     value = models.IntegerField()

#     objects = models.Manager()
