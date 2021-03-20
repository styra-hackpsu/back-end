from django.contrib import admin
from .models import UserEmotion, UserKeyword

# Register your models here.
admin.site.register(UserEmotion)
admin.site.register(UserKeyword)