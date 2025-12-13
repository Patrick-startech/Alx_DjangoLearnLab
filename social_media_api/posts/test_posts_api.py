# posts/tests/test_posts_api.py
from rest_framework.test import APITestCase
from django.urls import reverse
from accounts.models import User
from posts.models import Post

class PostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='patrick', password='SafePass123!')
        self.client.force_authenticate(self.user)

    def test_create_post(self):
        url = reverse('post-list')
        res = self.client.post(url, {'title': 'T1', 'content':'C1'}, format='json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)
