from config import settings
from django.db import models


class Course(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="название", help_text="введите название"
    )
    description = models.TextField(
        max_length=150,
        verbose_name="описание",
        help_text="введите описание",
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        upload_to="materials/pictures_courses",
        verbose_name="изображение",
        blank=True,
        null=True,
        help_text="Загрузите изображение курса",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        null=True,
        blank=True,
        help_text="Введите имя владельца",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    title = models.CharField(
        max_length=150, verbose_name="название", help_text="введите название"
    )
    description = models.TextField(
        max_length=150,
        verbose_name="описание",
        help_text="введите описание",
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        upload_to="materials/pictures_lessons",
        verbose_name="изображение",
        blank=True,
        null=True,
        help_text="загрузите изображение урока",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="урок", help_text="выберите курс"
    )
    url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Владелец",
        null=True,
        blank=True,
        help_text="Введите имя владельца",
    )

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
