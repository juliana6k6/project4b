from rest_framework import viewsets, generics

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):

    default_serializer = CourseSerializer
    # 2-ой способ
    # serializer_class = CourseSerializer
    queryset = Course.objects.all()
    serializers_choice = {'retrieve': CourseDetailSerializer}

    def get_serializer_class(self):
        """Определяем сериализатор с учетом запрашиваемого действия
         (self.action = list, retrieve, create, update,delete).
        Если действие не указано в словарике serializers_choice - используется default_serializer"""
        return self.serializers_choice.get(self.action, self.default_serializer)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonDeleteAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()