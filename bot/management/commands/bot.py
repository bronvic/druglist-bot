from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler

from django.core.management.base import BaseCommand

from bot.models import Drug


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
    )

def find_drug(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text.lower().capitalize()
    text = f'По вашему запросу "{user_text}" ничего не найдено'

    try:
        drug = Drug.objects.get(names__contains=[user_text])
        categories = ' '.join(drug.categories.values_list('smile', flat=True))

        text_parts = [f'Название: {user_text} {categories}']

        if len(drug.names) > 1:
            analogs = ', '.join(filter(lambda name: name != user_text, drug.names))
            text_parts.append(f'Аналоги: {analogs}')

        text_parts.append(f'\nОписание: {drug.description}')

        text = '\n'.join(text_parts)
    except Drug.DoesNotExist:
        pass

    update.message.reply_text(text)


class Command(BaseCommand):
    help = 'run telegram bot'

    def handle(self, *args, **kwargs):
        print('bot is running\n')

        # TODO: token
        updater = Updater('set token here')
        dispatcher = updater.dispatcher


        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(MessageHandler(Filters.text, find_drug))

        updater.start_polling()

        updater.idle()

