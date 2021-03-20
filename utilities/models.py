from django.db import models


# Create your models here.
class UserEmotion(models.Model):
    timestamp = models.DateTimeField('record date')
    emotions = models.JSONField('emotions')


class UserKeyword(models.Model):
    timestamp = models.DateTimeField('record date')
    keywords = models.JSONField('keywords')
    url = models.URLField('url', max_length=500)