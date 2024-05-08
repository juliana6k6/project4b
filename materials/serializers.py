from rest_framework import serializers

from materials.models import Course, Lesson
from rest_framework.fields import SerializerMethodField


class CourseSerializer(serializers.ModelSerializer):

    # 2-ой способ
    # lesson_count = serializers.SerializerMethodField()

    # def get_lesson_count(self, instance):
    #     if instance.lesson_set.all().first():
    #         return instance.lesson_set.all().count()
    #     return 0

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons_in_course = SerializerMethodField()

    @staticmethod
    def get_count_lessons_in_course(course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = "__all__"

