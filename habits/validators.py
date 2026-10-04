from rest_framework import serializers


def validate_habit(data):
    """Проверка всех правил для привычки."""
    is_pleasant = data.get('is_pleasant', False)
    related_habit = data.get('related_habit')
    reward = data.get('reward')
    duration = data.get('duration', 60)
    periodicity = data.get('periodicity', 1)

    errors = {}

    # 1. Нельзя одновременно связанную привычку и вознаграждение
    if related_habit and reward:
        errors['non_field_errors'] = 'Нельзя одновременно указывать связанную привычку и вознаграждение.'

    # 2. Время выполнения не больше 120 секунд
    if duration > 120:
        errors['duration'] = 'Время выполнения не должно превышать 120 секунд.'

    # 3. В связанные привычки — только приятные
    if related_habit and not related_habit.is_pleasant:
        errors['related_habit'] = 'Связанной может быть только приятная привычка.'

    # 4. Приятная привычка не имеет вознаграждения или связанной привычки
    if is_pleasant:
        if reward:
            errors['reward'] = 'У приятной привычки не может быть вознаграждения.'
        if related_habit:
            errors['related_habit'] = 'У приятной привычки не может быть связанной привычки.'

    # 5. Периодичность не реже 1 раза в 7 дней
    if periodicity > 7:
        errors['periodicity'] = 'Нельзя выполнять привычку реже, чем 1 раз в 7 дней.'

    if errors:
        raise serializers.ValidationError(errors)
