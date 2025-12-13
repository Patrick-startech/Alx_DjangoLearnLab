# posts/tests/test_feed.py
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User
from posts.models import Post

class FeedTests(APITestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username='alice', password='Pass123!')
        self.bob = User.objects.create_user(username='bob', password='Pass123!')
        self.client.force_authenticate(self.alice)
        self.alice.following.add(self.bob)
        Post.objects.create(author=self.bob, title='T1', content='C1')

    def test_feed_lists_followed_posts(self):
        url = reverse('feed')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['count'], 1)
        self.assertEqual(res.data['results'][0]['title'], 'T1')
