from rest_framework import serializers
from .models import Habit
from .validators import validate_habit


class HabitSerializer(serializers.ModelSerializer):
    """Полный сериализатор для привычек (CRUD)."""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['user']
        validators = [validate_habit]

    def validate(self, data):
        if self.instance:
            merged = {**self.__class__(self.instance).data, **data}
            validate_habit(merged)
        else:
            validate_habit(data)
        return data


class PublicHabitSerializer(serializers.ModelSerializer):
    """Только для чтения публичных привычек."""

    class Meta:
        model = Habit
        fields = ['id', 'place', 'time', 'action', 'duration', 'periodicity']
