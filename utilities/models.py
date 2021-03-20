from django.db import models


# Create your models here.
class UserEmotions(models.Model):
    timestamp = models.DateTimeField('record date')
    emotions = models.JSONField('emotions')


class UserKeywords(models.Model):
    timestamp = models.DateTimeField('record date')
    keywords = models.JSONField('keywords')
    url = models.URLField('url', max_length=500)