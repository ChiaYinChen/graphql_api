from django.contrib.auth.models import User
from django.db import models


class Article(models.Model):

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
