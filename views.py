import django.template
import telebot
from forrest_app.bot import bot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from settings import BOT_TOKEN

@csrf_exempt
def process_update(request) -> HttpResponse:
    if request.method == 'POST':
        json_string = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        print(request, 'GET_MESSAGE')
        return HttpResponse('!', 200)
    else:
        return HttpResponse('Method Not Allowed', 405)

bot.remove_webhook()
bot.set_webhook(url=f'hackathon.h1km4t1ll0.space/{BOT_TOKEN}')
