from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions

import services.api
from .models import UserEmotion, UserKeyword
from .serializers import UserEmotionSerializer, UserKeywordSerializer

# Create your views here.
def index(request):
    return HttpResponse("OK")


class FaceDetect(APIView):
    def post(self, request):
        res = services.api.face_detect(request.data.get("path"), request.data.get("choice"))
        obj = UserEmotion(timestamp=timezone.now(), emotions=res)
        obj.save()
        return Response(res)     



class UserEmotionViewSet(viewsets.ModelViewSet):
    queryset = UserEmotion.objects.all().order_by('timestamp')
    serializer_class = UserEmotionSerializer


class UserKeywordViewSet(viewsets.ModelViewSet):
    queryset = UserKeyword.objects.all().order_by('timestamp')
    serializer_class = UserKeywordSerializer
