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
        url = reverse("materials:lesson-create")
        data = {'title': 'Lesson1', 'description': 'Description_test',
                'course': self.course.id, 'url': 'https://course1.youtube.com/',
                'owner': self.user.id}
        response = self.client.post(url, data)
        print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(response.json(), {'id': 2, 'url': 'https://course1.youtube.com/', 'title': 'Lesson1',
                                           'description': 'Description_test', 'preview': None, 'course': 1, 'owner': 1})

    def test_lesson_retrieve(self):
        """Тестирование просмотра информации об уроке"""
        url = reverse('materials:lesson-retrieve', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), self.lesson.title)

    def test_lesson_update(self):
        """Тестирование редактирования урока"""
        url = reverse('materials:lesson-update',  args=(self.lesson.pk,))
        data = {'title': 'Lesson1_update', 'description': 'Description_update'}
        response = self.client.patch(url, data)
        data1 = response.json
        print(data1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.lesson.refresh_from_db()
        self.assertEqual(data.get('title'), "Lesson1_update")

    def test_lesson_delete(self):
        """Тестирование удаления урока"""
        url = reverse('materials:lesson-delete', args=(self.lesson.pk,))
        response = self.client.delete(url)
        print(f"{self.lesson.title} удалён")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

        # self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_lesson_list(self):
        url = reverse('materials:lesson-list')
        response = self.client.get(url)
        data = response.json
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)