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


class Group(models.Model):
    group_chat_id = models.BigIntegerField(primary_key=True,
                                           verbose_name='ID чата в ТГ',
                                           null=False,
                                           blank=False
                                           )
    '''имя группы, учеьное заведение, курс, факультет
    добавить ввод этих полей в боте'''
    admins = models.ManyToManyField(to=AdminBotUser,
                                    related_name='groups',
                                    verbose_name='Администраторы чата',
                                    null=False,
                                    blank=False
                                    )

    objects = models.Manager()

    def __str__(self) -> str:
        return f'#{str(self.group_chat_id)[1:]}'

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Teacher(models.Model):
    first_name = models.TextField(verbose_name='Имя',
                                  null=False,
                                  blank=False)

    second_name = models.TextField(verbose_name='Фамилия',
                                   null=False,
                                   blank=False)

    last_name = models.TextField(verbose_name='Отчество',
                                 null=False,
                                 blank=False)

    contact = models.TextField(verbose_name='Контакты',
                               null=False,
                               blank=False)

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{self.first_name} {self.second_name}'

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'


class Discipline(models.Model):
    short_name = models.TextField(verbose_name='Краткое название',
                                  null=False,
                                  blank=False)

    full_name = models.TextField(verbose_name='Полное название',
                                 null=False,
                                 blank=False)

    teacher = models.OneToOneField(Teacher,
                                   on_delete=models.CASCADE,
                                   null=False,
                                   blank=False)

    default_room = models.TextField(verbose_name='Аудитория',
                                    null=False,
                                    blank=False)

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{self.short_name}'

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class TimeBot(models.Model):
    name = models.TextField(verbose_name='Номер пары',
                            null=False,
                            blank=False)

    start = models.TextField(verbose_name='Начало',
                             null=False,
                             blank=False)
    end = models.TextField(verbose_name='Конец',
                           null=False,
                           blank=False)

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Время пар'
        verbose_name_plural = 'Время пар'


class Timetable(models.Model):
    discipline = models.OneToOneField(Discipline,
                                      on_delete=models.CASCADE,
                                      verbose_name='Дисциплина',
                                      null=False,
                                      blank=False)

    room = models.TextField(verbose_name='Аудитория',
                            null=False,
                            blank=False)

    week_day = models.IntegerField(choices=((1, 'Понедельник'),
                                            (2, 'Вторник'),
                                            (3, 'Среда'),
                                            (4, 'Четверг'),
                                            (5, 'Пятница'),
                                            (6, 'Суббота')),
                                   verbose_name='День недели',
                                   null=False,
                                   blank=False
                                   )

    week_type = models.BooleanField(choices=((True, 'Четная'),
                                             (False, 'Нечетная')),
                                    verbose_name='Четность недели',
                                    null=False,
                                    blank=False
                                    )

    time = models.OneToOneField(TimeBot,
                                on_delete=models.CASCADE,
                                verbose_name='Время',
                                null=False,
                                blank=False
                                )

    group = models.ForeignKey(to=Group,
                              on_delete=models.CASCADE,
                              default=None,
                              verbose_name='Группа')

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{self.discipline.short_name} {self.time}'

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class HomeworkType(models.Model):
    name = models.TextField(verbose_name='Тип домашней работы',
                            null=False,
                            blank=False)

    objects = models.Manager()

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Тип домашнего задания'
        verbose_name_plural = 'Типы домашнего задания'


class Homework(models.Model):
    id = models.TextField(primary_key=True,
                          null=False,
                          blank=False,
                          verbose_name='Номер домашнего задания',
                          auto_created=True)

    exp_date = models.TextField(verbose_name='Дедлайн',
                                null=False,
                                blank=False
                                )

    type = models.OneToOneField(HomeworkType,
                                on_delete=models.CASCADE,
                                verbose_name='Тип домашней работы',
                                null=False,
                                blank=False
                                )

    subject = models.OneToOneField(Discipline,
                                   on_delete=models.CASCADE,
                                   verbose_name='Дисциплина',
                                   null=False,
                                   blank=False
                                   )

    description = models.TextField(verbose_name='Описание',
                                   null=False,
                                   blank=False)

    group = models.ForeignKey(to=Group,
                              on_delete=models.CASCADE,
                              default=None,
                              verbose_name='Группа'
                              )

    objects = models.Manager()

    def __str__(self) -> str:
        return f'#{self.id} {self.subject.short_name}'

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'
