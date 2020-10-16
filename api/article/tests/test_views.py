from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from api.models import Article, Category, ArticleCategory

from api.util import random_text


def generate_article(previous_article=None, next_article=None, published=True) -> Article:
    return Article.objects.create(
        title=random_text(),
        preview_text=random_text(),
        text=random_text(),
        icon=None,
        previous_article=previous_article,
        next_article=next_article,
        published=published
    )


def generate_category() -> Category:
    return Category.objects.create(
        name=random_text(),
        icon=None,
        description=random_text()
    )


class TestArticleView(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.article1 = generate_article()
        self.article2 = generate_article()
        self.article3 = generate_article(published=False)

        self.category1 = generate_category()
        self.category2 = generate_category()

        self.admin = User.objects.create(
            is_superuser=True,
            is_staff=True,
            email=random_text(),
            username=random_text()
        )

    def test_all_articles_shortened_response_with_authenticated_user(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(f"/api/articles/{-1}/all_articles_shortened/")
        response2 = self.client.get(f"/api/articles/{self.article1.id}/all_articles_shortened/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 2)

    def test_all_articles_shortened_response_without_authenticated_user(self):
        response = self.client.get(f"/api/articles/{-1}/all_articles_shortened/")
        response2 = self.client.get(f"/api/articles/{self.article1.id}/all_articles_shortened/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_articles_response_with_authenticated_user(self):
        self.client.force_authenticate(self.admin)

        response = self.client.get(f"/api/articles/{-1}/all_articles/")
        response2 = self.client.get(f"/api/articles/{self.article1.id}/all_articles/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertIsNotNone(response.data[0]['text'])

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 2)
        self.assertIsNotNone(response2.data[0]['text'])

    def test_all_articles_response_without_authenticated_user(self):
        response = self.client.get(f"/api/articles/{-1}/all_articles/")
        response2 = self.client.get(f"/api/articles/{self.article1.id}/all_articles/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_published_response_without_authenticated_user(self):
        response = self.client.get('/api/articles/all_published/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertIsNotNone(response.data[0]['text'])

    def test_published_response_without_authenticated_user(self):
        response = self.client.get(f'/api/articles/{self.article1.id}/published/')
        response2 = self.client.get(f'/api/articles/{self.article3.id}/published/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['text'])

        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)

    def test_by_category_response_without_authenticated_user(self):
        self.article1.set_categories([self.category1.id])
        self.article2.set_categories([self.category2.id])

        self.article3.set_categories([self.category1.id, self.category2.id])

        response = self.client.get(f'/api/articles/{self.category1.id}/by_category/')
        response2 = self.client.get(f'/api/articles/{self.category2.id}/by_category/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data), 1)

    def test_edit_categories_response_with_authenticated_user(self):
        self.client.force_authenticate(self.admin)

        response = self.client.post(f'/api/articles/{self.article1.id}/edit_categories/',
                                    {"categories": f"[{self.category1.id}, {self.category2.id}]"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ArticleCategory.objects.filter(article=self.article1).count(), 2)