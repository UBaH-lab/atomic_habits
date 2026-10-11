from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from users.models import User
from .models import Habit


class HabitCRUDTestCase(TestCase):
    """Тесты CRUD для привычек."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='testpass123'
        )
        # Логинимся и получаем токен
        resp = self.client.post(
            '/api/login/',
            data={'email': 'test@test.com', 'password': 'testpass123'},
            format='json'
        )
        self.token = resp.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_habit(self):
        """Создание привычки."""
        data = {
            'place': 'Дом',
            'time': '08:00',
            'action': 'Попить воды',
            'duration': 60,
            'periodicity': 1
        }
        resp = self.client.post('/api/habits/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().user, self.user)

    def test_list_habits(self):
        """Список своих привычек."""
        Habit.objects.create(
            user=self.user, place='Дом', time='08:00',
            action='Попить воды', duration=60, periodicity=1
        )
        resp = self.client.get('/api/habits/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['count'], 1)

    def test_update_habit(self):
        """Обновление привычки."""
        habit = Habit.objects.create(
            user=self.user, place='Дом', time='08:00',
            action='Попить воды', duration=60, periodicity=1
        )
        resp = self.client.patch(
            f'/api/habits/{habit.id}/',
            {'place': 'Работа'},
            format='json'
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.get(id=habit.id).place, 'Работа')

    def test_delete_habit(self):
        """Удаление привычки."""
        habit = Habit.objects.create(
            user=self.user, place='Дом', time='08:00',
            action='Попить воды', duration=60, periodicity=1
        )
        resp = self.client.delete(f'/api/habits/{habit.id}/')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_cannot_access_other_user_habit(self):
        """Нельзя получить чужую привычку."""
        other = User.objects.create_user(
            email='other@test.com', username='other', password='pass123'
        )
        habit = Habit.objects.create(
            user=other, place='Парк', time='07:00',
            action='Пробежка', duration=120, periodicity=1
        )
        resp = self.client.get(f'/api/habits/{habit.id}/')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


class HabitValidatorTestCase(TestCase):
    """Тесты валидаторов привычек."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.com', username='testuser', password='testpass123'
        )
        resp = self.client.post(
            '/api/login/',
            data={'email': 'test@test.com', 'password': 'testpass123'},
            format='json'
        )
        self.token = resp.json()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_cannot_have_reward_and_related_habit(self):
        """Нельзя указать и награду, и связанную привычку."""
        related = Habit.objects.create(
            user=self.user, place='Дом', time='08:00',
            action='Медитация', duration=60, periodicity=1,
            is_pleasant=True
        )
        data = {
            'place': 'Дом', 'time': '09:00', 'action': 'Зарядка',
            'duration': 60, 'periodicity': 1,
            'reward': 'Шоколадка',
            'related_habit': related.id
        }
        resp = self.client.post('/api/habits/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_duration_max_120(self):
        """Время выполнения не больше 120 секунд."""
        data = {
            'place': 'Дом', 'time': '08:00', 'action': 'Попить воды',
            'duration': 200, 'periodicity': 1
        }
        resp = self.client.post('/api/habits/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_min_1(self):
        """Периодичность не меньше 1 раза в 7 дней."""
        data = {
            'place': 'Дом', 'time': '08:00', 'action': 'Попить воды',
            'duration': 60, 'periodicity': 0
        }
        resp = self.client.post('/api/habits/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_related_habit_must_be_pleasant(self):
        """Связанная привычка должна быть приятной."""
        related = Habit.objects.create(
            user=self.user, place='Дом', time='08:00',
            action='Отжимания', duration=60, periodicity=1,
            is_pleasant=False
        )
        data = {
            'place': 'Дом', 'time': '09:00', 'action': 'Зарядка',
            'duration': 60, 'periodicity': 1,
            'related_habit': related.id
        }
        resp = self.client.post('/api/habits/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class PublicHabitTestCase(TestCase):
    """Тесты публичных привычек."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.com', username='testuser', password='testpass123'
        )
        Habit.objects.create(
            user=self.user, place='Парк', time='07:00',
            action='Пробежка', duration=120, periodicity=1,
            is_public=True
        )
        Habit.objects.create(
            user=self.user, place='Дом', time='22:00',
            action='Чтение', duration=120, periodicity=1,
            is_public=False
        )

    def test_public_list_anonymous(self):
        """Аноним может видеть только публичные привычки."""
        resp = self.client.get('/api/habits/public/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()['count'], 1)
        self.assertEqual(resp.json()['results'][0]['action'], 'Пробежка')


class UserRegistrationTestCase(TestCase):
    """Тесты регистрации пользователя."""

    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        """Регистрация нового пользователя."""
        data = {
            'email': 'new@test.com',
            'username': 'newuser',
            'password': 'newpass123'
        }
        resp = self.client.post('/api/register/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='new@test.com').exists())

    def test_register_duplicate_email(self):
        """Нельзя зарегистрировать один email дважды."""
        User.objects.create_user(
            email='dup@test.com', username='dup', password='pass123'
        )
        data = {
            'email': 'dup@test.com',
            'username': 'another',
            'password': 'pass123'
        }
        resp = self.client.post('/api/register/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
