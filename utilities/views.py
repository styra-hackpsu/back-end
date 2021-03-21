from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
import math
import json
import datetime

import services.api
from .models import UserEmotion, UserKeyword
from .serializers import UserEmotionSerializer, UserKeywordSerializer


# send pk to record response later
class FaceDetect(APIView):
    def post(self, request):
        '''
        RETURNS res object (See db for sample return under USER EMOTION) (API Call from services/api/face_detect)
        '''
        res = services.api.face_detect(request.data.get("path"), request.data.get("choice"))
        print("FACE DETECT RESULT")
        print(res)
        
        # TODO: INCLUDE MODEL HERE
        model_prediction = "alert"
        print("MODEL PREDICTION", model_prediction)

        obj = UserEmotion(timestamp=timezone.now(), emotions=res, prediction=model_prediction)
        obj.save()
        res["pk"] = obj.pk;

        return Response(res)     


# send pk to record response later
class ChangeDetect(APIView):
    def post(self, request):
        '''
        RETURNS res object
        '''
        # Segregation between history just and history all
        JUST_LIM = 4
        ALL_LIM = 24
        MIN_ALL_LIM = 10

        res = UserKeyword.objects.all().order_by('-timestamp')[:ALL_LIM]

        # Min 3 Max 5 after Min 10 in history_all
        JUST_LIM = min(max(2, len(res) - MIN_ALL_LIM), 4)
        
        # maps a url to its json keywords
        history_all = dict()
        for obj in res[JUST_LIM:]:
            history_all[obj.url] = json.loads(obj.keywords)
        
        history_just = dict()
        for obj in res[:JUST_LIM]:
            history_just[obj.url] = json.loads(obj.keywords)

        current_keywords = services.api.getKeywords(request.data.get("url"))
        history_just[request.data.get("url")] = current_keywords
        
        if len(res) < 10:
            res = {"change_detected": "Not Enough Data"}
            print("CHANGE DETECT RESULT")
            print(res)       
            return Response(res)

        change_detected = services.api.detect_change(history_all=history_all, history_just=history_just)
        
        new_obj = UserKeyword(timestamp=timezone.now(), keywords=json.dumps(current_keywords), url=request.data.get("url"), prediction=change_detected)
        new_obj.save()

        print("HISTORY ALL")
        print(history_all)
        print("HISTORY JUST")
        print(history_just)

        res = {"pk": new_obj.pk, "change_detected": change_detected}
        print("CHANGE DETECT RESULT")
        print(res)

        return Response(res)

        
class UserEmotionViewSet(viewsets.ModelViewSet):
    queryset = UserEmotion.objects.all().order_by('-timestamp')
    serializer_class = UserEmotionSerializer


class UserKeywordViewSet(viewsets.ModelViewSet):
    queryset = UserKeyword.objects.all().order_by('-timestamp')
    serializer_class = UserKeywordSerializer


def index(request):
    return HttpResponse("OK")


# update user emotion response with GET
def update_user_emotion_response(request, pk, response):
    '''
    RETURNS status json
    '''
    status = {
        "status": "OK",
        "content": "None"
    }
    try:
        obj = UserEmotion.objects.get(pk=pk)
        obj.response = response
        print("RESPONSE FOR USER EMOTION", obj.pk, "IS", obj.response)
        obj.save()
    except Exception as e:
        print(e)
        status["status"] = "FAIL"
        status["content"] = str(e) 
        return HttpResponse(json.dumps(status))
    return HttpResponse(json.dumps(status))


# update user keyword response with GET
def update_user_keyword_response(request, pk, response):
    '''
    RETURNS status json
    '''
    status = {
        "status": "OK",
        "content": "None"
    }
    try:
        obj = UserKeyword.objects.get(pk=pk)
        obj.response = response
        print("RESPONSE FOR USER KEYWORD", obj.pk, "IS", obj.response)
        obj.save()
    except Exception as e:
        print(e)
        status["status"] = "FAIL"
        status["content"] = str(e) 
        return HttpResponse(json.dumps(status))
    return HttpResponse(json.dumps(status))


'''
RETURN FORMAT FOR ANALYSIS
{"user-keywords": [
    {
        "timestamp": --,
        "context-switch: --, (True/False)
    }
],
"user-emotions": [
    {
        "timestamp": --,
        "simple-emotions": {"additional_properties": {}, "anger": 0.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 1.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0},
        "complex-emotions": choice from ['non_vigilant', 'tired', 'alert']
    }
]
}
'''

def get_analysis_data(request):
    try:
        cur_date = datetime.date.today()
        prev_date = cur_date - datetime.timedelta(days=1)
        
        res = {
            "user-keywords": [],
            "user-emotions": []
        }
        
        # get user keywords
        objs1= UserKeyword.objects.filter(timestamp__range=[prev_date, cur_date])
        for obj in objs1:
            print(obj)
    except Exception as e:
        print(e)

    return HttpResponse("OK")
