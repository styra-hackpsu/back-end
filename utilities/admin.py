from django.contrib import admin
from .models import UserEmotions, UserKeywords

# Register your models here.
admin.site.register(UserEmotions)
admin.site.register(UserKeywords)