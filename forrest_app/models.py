from django.db import models


class AdminBotUser(models.Model):
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


class Value(models.Model):
    user = models.ForeignKey(to=AdminBotUser,
                             on_delete=models.CASCADE)
    key = models.CharField(max_length=50)
    value = models.IntegerField()

    objects = models.Manager()
