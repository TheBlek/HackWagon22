from django import forms

from .models import BotUser


class BotUserForm(forms.ModelForm):

    class Meta:
        model = BotUser
        fields = (
            'chat_id',
            'nickname',
            'full_name',
            'state'
        )
        widgets = {
            'nickname': forms.TextInput,
            'full_name': forms.TextInput,
        }
