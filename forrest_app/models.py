from django.db import models


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

    objects = models.Manager()

    def __str__(self) -> str:
        return f'#{self.telegram_id} @{self.nickname}'

    class Meta:
        verbose_name = 'Админ бота'
        verbose_name_plural = 'Админы бота'


'''class TmpGoods(models.Model)'''