from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from materials.models import Lesson, Course
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        """Создание и авторизация тестового пользователя"""
        self.user = User.objects.create(email='testov@test.ru', password='123abc')
        self.client.force_authenticate(user=self.user)
        """Создание тестового курса"""
        self.course = Course.objects.create(title='course_test', description='description_test', owner=self.user)
        """Создание тестового урока"""
        self.lesson = Lesson.objects.create(title='lesson_test', description='description_test',
                                            course=self.course, url='https://course.youtube.com/',
                                            owner=self.user)

    def test_lesson_create(self):
        """Тестирование создания урока"""
        url = reverse()
        data = {'title': 'Lesson1', 'description': 'Description_test',
                'course': self.course.id, 'url': 'https://course1.youtube.com/',
                'owner': self.user.id}
        response = self.client.post('/lesson/create/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.filter(name=data['name']).exists())

    def test_retrieve_lesson(self):
        """Тестирование просмотра информации об уроке"""
        path = reverse('materials:lesson_view', [self.lesson.id])
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_update_lesson(self):
        """Тестирование редактирования урока"""
        path = reverse('materials:lesson_update', [self.lesson.id])
        data = {'name': 'Updating_test', 'description': 'Updating_test'}
        response = self.client.patch(path, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, data['name'])

    def test_delete_lesson(self):
        """Проверка на права доступа - создан пользователь с правами
           модератора (не владелец урока)"""
        moderator = User.objects.create(id=2, email='moderator@test.ru',
                                        password='12345', role='moderator')
        self.client.force_authenticate(user=moderator)

        path = reverse('materials:lesson_delete', [self.lesson.id])
        response = self.client.delete(path)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # """asserts для успешного удаления урока"""
        # self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())