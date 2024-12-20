from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackContext,
    filters,
    MessageHandler,
)
from django.core.management.base import BaseCommand
from bot.models import Medicine, MedicineName
from asgiref.sync import sync_to_async
import os


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


def help_text() -> str:
    # categories_str = '\n'.join(map(lambda category: f'{category.smile} - {category.name}', Category.objects.all()))

    return (
        "Этот бот проверяет препараты на потенциальное отношение к фармакологической группе «фуфломицины»\n\n"
        "Если бот не находит лекарство в базе, значит есть вероятность того, что оно работает\n"
        "Если находит - значит с ним что-то не так. "
        "Список сформирован на основе отсутствия убедительных данных об эффективности препаратов по заявленным показаниям, "
        "как того требуют международные принципы доказательной медицины или по отсутствию в авторитетных источниках и рекомендациях\n\n"
        # 'В описании используются смайлики для удобства обозначения того что с данным препаратом не так:\n'
        # f'{categories_str}\n\n'
        "Информация взята с сайта https://encyclopatia.ru/wiki/Расстрельный_список_препаратов"
    )


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html(f"Привет!\n\n{help_text()}")


async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_html(help_text())


async def medicine_text(medicine_name: MedicineName) -> str:
    text_parts: list[str] = []
    text_parts.append(f"Название: <strong>{medicine_name.name}</strong>")

    alter_names = await sync_to_async(list)(
        MedicineName.objects.filter(description_id=medicine_name.description_id)
    )
    # Medicine has alternative names
    if len(alter_names) > 1:
        analogs = ", ".join(
            f"<em>{name.name}</em>"
            for name in alter_names
            if name != medicine_name.name
        )
        text_parts.append(f"Аналоги: {analogs}")

    medicine = await sync_to_async(Medicine.objects.get)(
        id=medicine_name.description_id
    )

    text_parts.append(f"\nОписание: {medicine.description}")

    return "\n".join(text_parts)


async def find_medicine(update: Update, context: CallbackContext) -> None:
    user_text = update.message.text.lower().capitalize()

    try:
        medicine_name = await sync_to_async(MedicineName.objects.get)(name=user_text)
        text = await medicine_text(medicine_name)
    except MedicineName.DoesNotExist:
        text = f"По вашему запросу <em>{user_text}</em> ничего не найдено"

    await update.message.reply_html(text, disable_web_page_preview=True)


class Command(BaseCommand):
    help = "run telegram bot"

    def handle(self, *args, **kwargs):
        print("bot is running\n")

        app = Application.builder().token(TELEGRAM_TOKEN).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("help", help))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_medicine))

        app.run_polling()
