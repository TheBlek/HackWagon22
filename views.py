import time
from django.http import HttpRequest, HttpResponse
from forrest_app.bot import bot


def run(request: HttpRequest) -> HttpResponse:
    try:
        bot.stop_polling()
        bot.polling(none_stop=True, interval=0)
    except Exception as _:
        time.sleep(1)
        bot.stop_polling()
        run(request)
    return HttpResponse(404)
