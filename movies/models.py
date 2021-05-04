from django.db import models
from django.contrib.postgres.fields import ArrayField

class movies(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    genres = models.CharField(max_length=100)
    uuid = models.IntegerField(default=0)

class favorite_genres(models.Model):
    favorite_genres = models.CharField(max_length=100)

class movieCollections(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    collections = models.ForeignKey(movies, on_delete=models.PROTECT)

class getCollections(models.Model):
    is_success = models.BooleanField(default=False)
    data = models.ForeignKey(movieCollections, on_delete=models.PROTECT)
    favorite_genres = models.ForeignKey(favorite_genres, on_delete=models.PROTECT)
