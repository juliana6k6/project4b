from materials.paginators import CoursePaginator
from rest_framework import viewsets, generics

from materials.models import Course, Lesson
from materials.serializers import (
    CourseSerializer,
    LessonSerializer,
    CourseDetailSerializer,
)
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModer, IsOwner
from materials.tasks import mail_update_course_info


class CourseViewSet(viewsets.ModelViewSet):

    default_serializer = CourseSerializer
    # 2-ой способ
    # serializer_class = CourseSerializer
    queryset = Course.objects.all()
    serializers_choice = {"retrieve": CourseDetailSerializer}
    pagination_class = CoursePaginator

    def get_serializer_class(self):
        """Определяем сериализатор с учетом запрашиваемого действия
         (self.action = list, retrieve, create, update,delete).
        Если действие не указано в словарике serializers_choice - используется default_serializer
        """
        return self.serializers_choice.get(self.action, self.default_serializer)

    def perform_create(self, serializer):
        """Привязываем текущего пользователя к создаваемому объекту"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        """Отправляем уведомление всем подписанным пользователям"""
        updated_course = serializer.save()
        mail_update_course_info.delay(updated_course)
        updated_course.save()

    def get_permissions(self):
        """Определяем права доступа с учетом запрашиваемого действия"""
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["retrieve", "update", "list"]:
            self.permission_classes = (
                IsModer | IsOwner,
            )  # модератор или владелец может просмотреть и редактировать
        elif self.action == "destroy":
            self.permission_classes = (
                ~IsModer | IsOwner,
            )  # немодератор или владелец может удалить
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        """Привязываем текущего пользователя к создаваемому объекту"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CoursePaginator


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)
