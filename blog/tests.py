import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from .models import Article


@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class BlogManualCheckTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="admin",
            password="adminpass123",
            is_staff=True,
            is_superuser=True,
        )
        cls.user = User.objects.create_user(
            username="user",
            password="userpass123",
            is_staff=False,
            is_superuser=False,
        )

        cls.published_article = Article.objects.create(
            titre="Article Public",
            contenu="Contenu public",
            date_publication=timezone.now(),
            auteur=cls.admin,
            statut="publie",
        )
        cls.draft_article = Article.objects.create(
            titre="Brouillon",
            contenu="Contenu brouillon",
            date_publication=timezone.now(),
            auteur=cls.admin,
            statut="brouillon",
        )

    @classmethod
    def tearDownClass(cls):
        media_root = getattr(cls, "MEDIA_ROOT", None)
        if media_root:
            shutil.rmtree(media_root, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client = Client()

    def test_home_lists_only_published_for_anonymous(self):
        response = self.client.get(reverse("article-list"))
        self.assertContains(response, self.published_article.titre)
        self.assertNotContains(response, self.draft_article.titre)

    def test_home_lists_all_for_authenticated(self):
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get(reverse("article-list"))
        self.assertContains(response, self.published_article.titre)
        self.assertContains(response, self.draft_article.titre)

    def test_detail_published_accessible(self):
        response = self.client.get(
            reverse("article-detail", kwargs={"pk": self.published_article.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_detail_draft_blocked_for_anonymous(self):
        response = self.client.get(
            reverse("article-detail", kwargs={"pk": self.draft_article.pk})
        )
        self.assertNotEqual(response.status_code, 200)

    def test_create_requires_login(self):
        response = self.client.get(reverse("article-create"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_create_with_image_as_admin(self):
        self.client.login(username="admin", password="adminpass123")
        image = SimpleUploadedFile(
            "test.jpg",
            b"\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x00\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B",
            content_type="image/gif",
        )
        response = self.client.post(
            reverse("article-create"),
            {
                "titre": "Article Image",
                "contenu": "Contenu avec image",
                "statut": "publie",
                "date_publication": timezone.now().strftime("%Y-%m-%dT%H:%M"),
                "image": image,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Article.objects.filter(titre="Article Image").exists())

    def test_update_requires_login(self):
        response = self.client.get(
            reverse("article-update", kwargs={"pk": self.published_article.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_delete_requires_login(self):
        response = self.client.get(
            reverse("article-delete", kwargs={"pk": self.published_article.pk})
        )
        self.assertEqual(response.status_code, 302)

# Create your tests here.
