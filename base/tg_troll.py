from background_task import background
from base.models import Setting
import telebot


@background
def send_troll(tg_id):
    setting = Setting.objects.all().last()
    bot = telebot.TeleBot(token=setting.tg_api)
    bot.send_message(tg_id, 'Я пришёл!')
