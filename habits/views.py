from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer
from .permissions import IsOwner
from .paginators import HabitPaginator
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets

@extend_schema(
    parameters=[
        OpenApiParameter(name='id', type=int, location=OpenApiParameter.PATH),
    ]
)

class HabitViewSet(viewsets.ModelViewSet):
    """CRUD для привычек текущего пользователя."""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """Только свои привычки."""
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Автоматически привязываем пользователя."""
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(generics.ListAPIView):
    """Список публичных привычек (только чтение)."""
    queryset = Habit.objects.filter(is_public=True)
    serializer_class = PublicHabitSerializer
    pagination_class = HabitPaginator
    permission_classes = [AllowAny]
    