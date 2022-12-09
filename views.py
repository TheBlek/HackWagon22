import time
from forrest_app.bot import bot


def run(request):
    try:
        bot.stop_polling()
        bot.polling(none_stop=True, interval=0)
    except Exception as _:
        time.sleep(1)
        bot.stop_polling()
        run(request)
