from django.db import models
from users.models import User


class Habit(models.Model):
    """Привычка — полезная или приятная."""

    PERIODICITY_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Раз в 2 дня'),
        (3, 'Раз в 3 дня'),
        (4, 'Раз в 4 дня'),
        (5, 'Раз в 5 дней'),
        (6, 'Раз в 6 дней'),
        (7, 'Раз в неделю'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )
    place = models.CharField(
        max_length=200,
        verbose_name='Место'
    )
    time = models.TimeField(
        verbose_name='Время выполнения'
    )
    action = models.CharField(
        max_length=300,
        verbose_name='Действие'
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_habits',
        verbose_name='Связанная привычка'
    )
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=1,
        verbose_name='Периодичность (дни)'
    )
    reward = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name='Вознаграждение'
    )
    duration = models.PositiveIntegerField(
        default=60,
        verbose_name='Время на выполнение (секунды)'
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['id']

    def __str__(self):
        return f'{self.user.email} — {self.action} в {self.time} в {self.place}'
