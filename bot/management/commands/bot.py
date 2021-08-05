from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

from django.core.management.base import BaseCommand


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
            fr'Hi {user.mention_markdown_v2()}\!',
        )


class Command(BaseCommand):
    help = 'run telegram bot'

    def handle(self, *args, **kwargs):
        print('bot is running\n')

        # TODO: token
        updater = Updater('set token here')

        updater.dispatcher.add_handler(CommandHandler('start', start))

        updater.start_polling()

        updater.idle()

