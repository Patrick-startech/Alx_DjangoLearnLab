from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Author, Book

User = get_user_model()

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="tester", password="pass12345")

        self.author1 = Author.objects.create(name="Toni Morrison")
        self.author2 = Author.objects.create(name="Chinua Achebe")

        self.book1 = Book.objects.create(title="Beloved", publication_year=1987, author=self.author1)
        self.book2 = Book.objects.create(title="Song of Solomon", publication_year=1977, author=self.author1)
        self.book3 = Book.objects.create(title="Things Fall Apart", publication_year=1958, author=self.author2)

        self.url_list = reverse("book-list")
        self.url_detail = lambda pk: reverse("book-detail", kwargs={"pk": pk})
        self.url_create = reverse("book-create")
        self.url_update = lambda pk: reverse("book-update", kwargs={"pk": pk})
        self.url_delete = lambda pk: reverse("book-delete", kwargs={"pk": pk})


class BookListTests(BaseAPITestCase):
    def test_list_books(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        titles = {b["title"] for b in response.data}
        self.assertTrue({"Beloved", "Song of Solomon", "Things Fall Apart"} <= titles)


class BookDetailTests(BaseAPITestCase):
    def test_retrieve_book(self):
        response = self.client.get(self.url_detail(self.book1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Beloved")
        self.assertEqual(response.data["author"], self.author1.id)


class BookCRUDTests(BaseAPITestCase):
    def test_create_book_requires_auth(self):
        payload = {"title": "Jazz", "publication_year": 1992, "author": self.author1.id}

        # Unauthenticated → 401/403
        res_unauth = self.client.post(self.url_create, payload, format="json")
        self.assertIn(res_unauth.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        # Authenticated → 201
        self.client.login(username="tester", password="pass12345")
        res_auth = self.client.post(self.url_create, payload, format="json")
        self.assertEqual(res_auth.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res_auth.data["title"], "Jazz")
        self.assertEqual(Book.objects.count(), 4)

    def test_update_book_requires_auth(self):
        payload = {"title": "Beloved (Updated)"}
        res_unauth = self.client.patch(self.url_update(self.book1.id), payload, format="json")
        self.assertIn(res_unauth.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        self.client.login(username="tester", password="pass12345")
        res_auth = self.client.patch(self.url_update(self.book1.id), payload, format="json")
        self.assertEqual(res_auth.status_code, status.HTTP_200_OK)
        self.assertEqual(res_auth.data["title"], "Beloved (Updated)")

    def test_delete_book_requires_auth(self):
        res_unauth = self.client.delete(self.url_delete(self.book2.id))
        self.assertIn(res_unauth.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

        self.client.login(username="tester", password="pass12345")
        res_auth = self.client.delete(self.url_delete(self.book2.id))
        self.assertEqual(res_auth.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())


class BookQueryCapabilitiesTests(BaseAPITestCase):
    def test_filter_by_title(self):
        res = self.client.get(self.url_list, {"title": "Beloved"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Beloved")

    def test_filter_by_author_id(self):
        res = self.client.get(self.url_list, {"author": self.author1.id})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertEqual(set(titles), {"Beloved", "Song of Solomon"})

    def test_filter_by_publication_year(self):
        res = self.client.get(self.url_list, {"publication_year": 1958})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Things Fall Apart")

    def test_search_title_partial(self):
        res = self.client.get(self.url_list, {"search": "Bel"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(any(b["title"] == "Beloved" for b in res.data))

    def test_search_author_name_partial(self):
        res = self.client.get(self.url_list, {"search": "achebe"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertEqual(set(titles), {"Things Fall Apart"})

    def test_ordering_by_title_asc(self):
        res = self.client.get(self.url_list, {"ordering": "title"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in res.data]
        self.assertEqual(titles, sorted(titles))

    def test_ordering_by_publication_year_desc(self):
        res = self.client.get(self.url_list, {"ordering": "-publication_year"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in res.data]
        self.assertEqual(years, sorted(years, reverse=True))
