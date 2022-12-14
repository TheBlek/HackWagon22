from django.contrib import admin

from .models import BotUser, Items
from .forms import BotUserForm


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'nickname', 'full_name', 'state')
    form = BotUserForm


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('user', 'detail', 'number', 'zavod', 'year')
