from materials.models import Course
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User, Subscription
from rest_framework.reverse import reverse


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testov@test.ru', password="123abc")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="Course5", description="Description",
                                            owner=self.user)

    def test_subscription_create(self):
        data = {"user": self.user.id, "course": self.course.id}
        url = reverse("users:sub_script")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка добавлена'})

    def test_subscription_delete(self):
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)
        data = {"user": self.user.id, "course": self.course.id}
        url = reverse("users:sub_script")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Подписка удалена'})
