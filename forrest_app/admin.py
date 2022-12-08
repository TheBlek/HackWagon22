from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.


@admin.register(Teacher)
class TeacherAmin(admin.ModelAdmin):
    list_display = ['first_name',
                    'second_name']

    list_filter = ('first_name',
                   'second_name',
                   'last_name')

    form = TeacherForm


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['short_name',
                    'teacher',
                    'default_room']

    list_filter = ('short_name',
                   'full_name')

    form = DisciplineForm


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['discipline',
                    'room',
                    'week_day',
                    'week_type',
                    'time']

    list_filter = ('room',
                   'week_day',
                   'week_type')

    form = TimetableForm


@admin.register(HomeworkType)
class HomeworkTypeAdmin(admin.ModelAdmin):
    list_display = ['name']

    form = HomeworkTypeForm


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'exp_date',
                    'type',
                    'subject',
                    'description']

    list_filter = ('exp_date',
                   'type',
                   'subject')

    form = HomeworkForm


@admin.register(AdminBotUser)
class AdminBotUserAdmin(admin.ModelAdmin):
    list_display = ['telegram_id',
                    'nickname',
                    'full_name']

    list_filter = ('nickname',
                   'full_name')

    form = AdminBotUserForm

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['group_chat_id',
                    'admins_']

    list_filter = ('group_chat_id',)

    form = GroupForm

    def admins_(self, group):
        admins = [str(admin_.full_name) for admin_ in group.admins.all()]

        if len(admins) > 1:
            return ', '.join(admins)
        elif len(admins) == 1:
            return admins[0]


@admin.register(TimeBot)
class TimeBotAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'start',
                    'end']

    form = TimeBotForm
