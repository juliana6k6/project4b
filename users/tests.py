from materials.models import Course
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, Subscription
from rest_framework.reverse import reverse


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='test5@test.ru', password="123qwe5")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Новый курс", description="Описание для нового курса",
                                            owner=self.user)

    def test_subscription_create(self):
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        url = reverse("users:sub_script")

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(), {'message': 'Подписка добавлена'}
        )

    def test_subscription_delete(self):
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)

        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        url = reverse("users:sub_script")

        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(), {'message': 'Подписка удалена'}
        )
# class SubscriptionTestCase(APITestCase):
#
#     def setUp(self):
#         """Создание и авторизация тестового пользователя"""
#         self.user = User.objects.create(email="juliana6k@gmail.com")
#         self.user.set_password('1234abcd')
#         self.client.force_authenticate(user=self.user)
#         """Создание тестового курса"""
#         self.course = Course.objects.create(title="Course_5", description="description_test", owner=self.user)
#
#     def test_sub_on(self):
#         """Тестирование добавления подписки (однократное
#            обращение к контроллеру)"""
#         url = reverse('users:sub_script', args=(self.course.pk,))
#         response = self.client.post(url)
#         print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], "Подписка добавлена")
#
#     def test_sub_off(self):
#         """Тестрование удаления подписки (двойное
#            обращение к контроллеру)"""
#         url = reverse('users:sub_script', args=(self.course.pk,))
#         response = self.client.post(url)
#         response = self.client.post(url)
#         print(response.json())
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['message'], "Подписка удалена")
#     # def test_subscribed(self):
#     #     url = reverse('users:sub_script', args=(self.course.pk,))
#     #     data = {"user": self.user.pk, "course": self.course.pk}
#     #     response = self.client.post(url, data)
#     #     data = response.json()
#     #     print(data)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(data, {'message': 'Подписка добавлена'})
#
#     # def test_subscription_create(self):
#     #     data = {
#     #         'course_id': self.course.id,
#     #     }
#     #     url = reverse('users:sub_script')
#     #     response = self.client.post(url, data)
#     #     print(response.json())
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(response.json().get('message'), 'подписка добавлена')
#     #
#     #     response = self.client.post(url, data)
#     #     self.assertEqual(response.json().get('message'), 'подписка удалена')
#     #     with self.assertRaises(Subscription.DoesNotExist):
#     #         Subscription.objects.get(course_id=self.course.id)
#     #
#
#     # def test_unsubscribed(self):
#     #     url = reverse('users:sub_script', args=(self.course.pk,))
#     #     Subscription.objects.create(course=self.course, user=self.user)
#     #     data = {"user": self.user.pk, "course": self.course.pk}
#     #     response = self.client.post(url, data)
#     #     data = response.json()
#     #     print(data)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(data, {'message': 'Подписка удалена'})
#
#     # def test_subscribed(self):
#     #     url = reverse('users:sub_script', args=(self.course.pk,))
#     #     data = {"user": self.user.pk, "course": self.course.pk}
#     #     response = self.client.post(url, data)
#     #     data = response.json()
#     #     print(data)
#     #     self.assertEqual(response.status_code, status.HTTP_200_OK)
#     #     self.assertEqual(data, {'message': 'Подписка добавлена'})
#
#     # def test_create_subscription(self):
#     #     """Тест создания подписки"""
#     #
#     #     data = {"user": self.user.pk, "course": self.course.pk}
#     #     response = self.client.post(reverse(":subscription_create"), data=data)
#     #
#     #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#     #
#     # def test_delete_subscription(self):
#     #     """Тест удаления подписки"""
#     #
#     #     self.client.delete(
#     #         reverse("education:subscription_delete", args=[self.course.id])
#     #     )
#     #
#     #     self.assertFalse(Subscription.objects.filter(id=self.course.id).exists())