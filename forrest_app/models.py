from django.db import models
from settings import BotStates


class BotUser(models.Model):
    chat_id = models.BigIntegerField(primary_key=True,
                                         verbose_name='ID телеграм чата',
                                         null=False,
                                         blank=False
                                         )

    nickname = models.TextField(verbose_name='Никнейм',
                                null=False,
                                blank=False)

    full_name = models.TextField(verbose_name='ФИО', null=False,
                                 blank=False)

    STATES = [
        (BotStates.REGISTRATION.value, BotStates.REGISTRATION.name),
        (BotStates.MAIN_MENU.value, BotStates.MAIN_MENU.name),
        (BotStates.RECORDING.value, BotStates.RECORDING.name),
        (BotStates.CONFIRMATION.value, BotStates.CONFIRMATION.name),
    ]

    state = models.IntegerField(verbose_name='Текущее состояние',
                                choices=STATES,
                                default=BotStates.REGISTRATION.value,
                                null=False,
                                blank=False)

    objects = models.Manager()

    def __str__(self) -> str:
        return f'#{self.chat_id} @{self.nickname}'

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'


class Items(models.Model):
    user = models.ForeignKey(to=BotUser,
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    count = models.IntegerField()

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{self.name} {self.count}шт'

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

class ItemsForConfirmation(models.Model):
    user = models.OneToOneField(to=BotUser,
                                on_delete=models.CASCADE)
    items = models.JSONField()

    objects = models.Manager()

