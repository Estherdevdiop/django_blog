from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Article(models.Model):

    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('publie', 'Publié'),
    ]

    titre = models.CharField(max_length=200, verbose_name="Titre")
    contenu = models.TextField(verbose_name="Contenu")
    date_publication = models.DateTimeField(default=timezone.now, verbose_name="Date de publication")
    auteur = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name="Image")
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='publie', verbose_name="Statut")

    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})