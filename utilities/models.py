from django.db import models


class UserEmotion(models.Model):
    timestamp = models.DateTimeField('timestamp')
    emotions = models.JSONField('emotions')
    prediction = models.JSONField('prediction') # Store the confidence of each prediction ? 
    response = models.CharField('response', max_length=200, default='None')

class UserKeyword(models.Model):
    timestamp = models.DateTimeField('timestamp')
    keywords = models.JSONField('keywords')
    url = models.URLField('url', max_length=500)
    prediction = models.BooleanField('prediction', default=False)
    response = models.CharField('response', max_length=200, default='None') # Needs a response in ("Yes","No")
