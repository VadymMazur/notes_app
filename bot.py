import os
import threading
import time

import django
import telebot

from config import BOT_TOKEN, CHANNEL_ID


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notes_app.settings')
django.setup()

from django.utils import timezone

from notes.models import Note


bot = telebot.TeleBot(BOT_TOKEN)


def get_note_text(note):
    return (
        f'Назва: {note.title}\n'
        f'Текст: {note.text}\n'
        f'Категорія: {note.category.title}\n'
        f'Дата нагадування: {note.reminder:%d.%m.%Y}'
    )


def send_created_notes():
    notes = Note.objects.select_related('category').filter(
        sent_to_telegram=False,
    )
    for note in notes:
        bot.send_message(
            CHANNEL_ID,
            f'Створено нову нотатку\n\n{get_note_text(note)}',
        )
        note.sent_to_telegram = True
        note.save(update_fields=['sent_to_telegram'])


def send_scheduled_notifications():
    notes = Note.objects.select_related('category').filter(
        reminder__lte=timezone.localdate(),
        reminder_sent=False,
    )
    for note in notes:
        bot.send_message(
            CHANNEL_ID,
            f'Нагадування\n\n{get_note_text(note)}',
        )
        note.reminder_sent = True
        note.save(update_fields=['reminder_sent'])


def notification_scheduler():
    while True:
        send_created_notes()
        send_scheduled_notifications()
        time.sleep(60)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Бот нотаток запущено.',
    )


if __name__ == '__main__':
    scheduler = threading.Thread(
        target=notification_scheduler,
        daemon=True,
    )
    scheduler.start()
    print('Бот запущено...')
    bot.polling(none_stop=True)
