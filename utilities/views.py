from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
import json

import services.api
from .models import UserEmotion, UserKeyword
from .serializers import UserEmotionSerializer, UserKeywordSerializer

# Create your views here.
def index(request):
    return HttpResponse("OK")

class FaceDetect(APIView):
    def post(self, request):
        res = services.api.face_detect(request.data.get("path"), request.data.get("choice"))
        print("FACE DETECT RESULT")
        print(res)
        obj = UserEmotion(timestamp=timezone.now(), emotions=res)
        obj.save()
        return Response(res)     


class ChangeDetect(APIView):
    def post(self, request):

        # Segregation between history just and history all
        JUST_LIM = 4
        ALL_LIM = 24

        res = UserKeyword.objects.all().order_by('-timestamp')[:ALL_LIM]
        # maps a url to its json keywords
        history_all = dict()
        for obj in res[JUST_LIM:]:
            history_all[obj.url] = json.loads(obj.keywords)
        
        history_just = dict()
        for obj in res[:JUST_LIM]:
            history_just[obj.url] = json.loads(obj.keywords)

        current_keywords = services.api.getKeywords(request.data.get("url"))
        history_just[request.data.get("url")] = current_keywords
        
        new_obj = UserKeyword(timestamp=timezone.now(), keywords=json.dumps(current_keywords), url=request.data.get("url"))
        new_obj.save()

        print("HISTORY ALL")
        print(history_all)
        print("HISTORY JUST")
        print(history_just)

        res = {"change_detected": services.api.detect_change(history_all=history_all, history_just=history_just)}
        return Response(res)

        
class UserEmotionViewSet(viewsets.ModelViewSet):
    queryset = UserEmotion.objects.all().order_by('timestamp')
    serializer_class = UserEmotionSerializer


class UserKeywordViewSet(viewsets.ModelViewSet):
    queryset = UserKeyword.objects.all().order_by('timestamp')
    serializer_class = UserKeywordSerializer
