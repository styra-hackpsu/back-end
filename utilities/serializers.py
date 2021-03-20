from rest_framework import serializers
from .models import UserEmotion, UserKeyword


class UserEmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmotion
        fields = '__all__'
    

class UserKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserKeyword
        fields = '__all__'