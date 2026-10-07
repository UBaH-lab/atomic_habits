from celery import shared_task
from django.utils import timezone
from .models import Habit
from .services import send_telegram_message


@shared_task
def send_habit_reminder():
    """Периодическая задача — проверяет, кому нужно напомнить о привычке."""
    now = timezone.now()
    current_time = now.time().replace(second=0, microsecond=0)

    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
        time__hour=current_time.hour,
        time__minute=current_time.minute,
    )

    for habit in habits:
        message = (
            f"⏰ Напоминание!\n"
            f"Я буду {habit.action} в {habit.time} в {habit.place}."
        )
        send_telegram_message(
            chat_id=habit.user.telegram_chat_id,
            text=message
        )

    return f"Reminders checked, sent to {habits.count()} users"
