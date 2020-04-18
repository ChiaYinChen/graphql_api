from django.db import models


class Article(models.Model):

    title = models.CharField(max_length=250)
    content = models.TextField()
    url = models.URLField()

    class Meta:
        db_table = 'article'
