# notifications/tests/test_notifications.py
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User
from notifications.models import Notification

class NotificationsTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='Pass123!')
        self.client.force_authenticate(self.alice)
        Notification.objects.create(recipient=self.alice, actor=None, verb='followed')

    def test_list_notifications(self):
        url = reverse('notifications')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 1)
