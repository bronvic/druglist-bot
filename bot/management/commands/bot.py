from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, Filters, MessageHandler

from django.core.management.base import BaseCommand

from bot.models import Drug, Category


def help_text() -> str:
    categories_str = '\n'.join(map(lambda category: f'{category.smile} - {category.name}', Category.objects.all()))

    return (
        'Этот бот проверяет препараты на потенциальное отношение к фармакологической группе «фуфломицины»\n\n'
        'Если бот не находит лекарство в базе, значит есть вероятность того, что оно работает\n'
        'Если находит - значит с ним что-то не так. '
        'Список сформирован на основе отсутствия убедительных данных об эффективности препаратов по заявленным показаниям, '
        'как того требуют международные принципы доказательной медицины или по отсутствию в авторитетных источниках и рекомендациях\n\n'
        'В описании используются смайлики для удобства обозначения того что с данным препаратом не так:\n'
        f'{categories_str}\n\n'
        'Информация взята с сайта https://encyclopatia.ru/wiki/Расстрельный_список_препаратов'
    )

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_html(f'Привет!\n\n{help_text()}')

def help(update: Update, context: CallbackContext) -> None:
    update.message.reply_html(help_text())

def drug_text(drug: Drug, search_name: str) -> str:
    text_parts: list[str] = []

    # Get categories for given drug
    categories = ' '.join(drug.categories.values_list('smile', flat=True))

    # Text for drug name and it's categories
    text_parts.append(f'Название: <strong>{search_name}</strong> {categories}')

    # Text for drug analogs, if any
    if len(drug.names) > 1:
        analogs = ', '.join(map(lambda analog: f'<em>{analog}</em>', filter(lambda name: name != search_name, drug.names)))
        text_parts.append(f'Аналоги: {analogs}')

    # Text for drug description
    text_parts.append(f'\nОписание: {drug.description}')

    return '\n'.join(text_parts)

def find_drug(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text.lower().capitalize()

    try:
        drug = Drug.objects.get(names__contains=[user_text])
        text = drug_text(drug, user_text)
    except Drug.DoesNotExist:
        text = f'По вашему запросу <em>{user_text}</em> ничего не найдено'

    update.message.reply_html(text, disable_web_page_preview=True)


class Command(BaseCommand):
    help = 'run telegram bot'

    def handle(self, *args, **kwargs):
        print('bot is running\n')

        # TODO: token
        updater = Updater('set token here')
        dispatcher = updater.dispatcher


        dispatcher.add_handler(CommandHandler('start', start))
        dispatcher.add_handler(CommandHandler('help', help))
        dispatcher.add_handler(MessageHandler(Filters.text, find_drug))

        updater.start_polling()

        updater.idle()

