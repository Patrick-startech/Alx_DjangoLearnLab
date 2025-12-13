# posts/tests/test_likes.py
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User
from posts.models import Post, Like
from notifications.models import Notification

class LikesTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='Pass123!')
        self.bob = User.objects.create_user(username='bob', password='Pass123!')
        self.client.force_authenticate(self.alice)
        self.post = Post.objects.create(author=self.bob, title='T', content='C')

    def test_like_creates_notification(self):
        url = reverse('post-like', args=[self.post.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Notification.objects.filter(recipient=self.bob, verb='liked').count(), 1)

    def test_unlike(self):
        Like.objects.create(user=self.alice, post=self.post)
        url = reverse('post-unlike', args=[self.post.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Like.objects.count(), 0)
