# accounts/tests/test_follows.py
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User

class FollowsTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='Pass123!')
        self.bob = User.objects.create_user(username='bob', password='Pass123!')
        self.client.force_authenticate(self.alice)

    def test_follow_unfollow(self):
        follow_url = reverse('follow-user', args=[self.bob.id])
        unfollow_url = reverse('unfollow-user', args=[self.bob.id])
        self.client.post(follow_url)
        self.assertTrue(self.bob in self.alice.following.all())
        self.client.post(unfollow_url)
        self.assertFalse(self.bob in self.alice.following.all())
