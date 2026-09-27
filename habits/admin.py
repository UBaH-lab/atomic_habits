from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'place', 'time', 'user', 'is_public', 'is_pleasant')
    list_filter = ('is_public', 'is_pleasant')
    search_fields = ('action', 'place')
