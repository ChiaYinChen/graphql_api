"""Posts app models."""
from django.db import models

from users.models import User


class Article(models.Model):
    """Table for article."""

    title = models.CharField(max_length=250)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    content = models.TextField()
    url = models.URLField()

    class Meta:
        db_table = 'article'
