from django.contrib import admin

from .models import BotUser
from .forms import BotUserForm


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'nickname', 'full_name', 'state')
    form = BotUserForm
