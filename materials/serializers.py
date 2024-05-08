from rest_framework import serializers

from materials.models import Course, Lesson
from rest_framework.fields import SerializerMethodField


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    count_lessons_in_course = SerializerMethodField()

    @staticmethod
    def get_count_lessons_in_course(course):
        return Lesson.objects.filter(course=course).count()

    # def get_lesson_count(self, instance):
    #     return instance.lesson_set.count()

    # 2-ой способ
    # lesson_count = serializers.SerializerMethodField()

    # def get_lesson_count(self, instance):
    #     if instance.lesson_set.all().first():
    #         return instance.lesson_set.all().count()
    #     return 0

    class Meta:
        model = Course
        fields = '__all__'



class CourseDetailSerializer(serializers.ModelSerializer):
    count_lessons_in_course = SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)

    @staticmethod
    def get_count_lessons_in_course(course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = "__all__"

