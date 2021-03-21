from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status

import math
import json
import datetime
from django.utils import timezone

import services.api
import services.emotion_model.model
from .models import UserEmotion, UserKeyword
from .serializers import UserEmotionSerializer, UserKeywordSerializer


# NOTE THE USE OF "None" for features that haven't been recorded

PREDICTION = {0: "alert",  1: "non_vigilant",  2: "tired"}
ORDER_EMOTIONS = ['anger','contempt','disgust','fear','happiness','neutral','sadness','surprise']
FILE_PATH = './utilities/storage.txt'
# Segregation between history just and history all
JUST_LIM = 4
ALL_LIM = 24
MIN_ALL_LIM = 10



# send pk to record response later
class FaceDetect(APIView):
    def post(self, request):
        '''
        RETURNS res object (See db for sample return under USER EMOTION) (API Call from services/api/face_detect)
        '''
        try:
            res = services.api.face_detect(request.data.get("path"), request.data.get("choice"))
        except Exception as e:
            print(f"Exception in face_detect: {e}")
            return Response({'error': "Could not detect faces."}, status = status.HTTP_400_BAD_REQUEST)
        

        print("FACE DETECT RESULT")
        print(res)
        
        # TODO: INCLUDE MODEL HERE
        model_input = [float(res['emotion'][x]) for x in ORDER_EMOTIONS]
        print("MODEL INPUT", model_input)
        model_result = services.emotion_model.model.predict(model_input)
        model_prediction = dict()
        for i in range(len(model_result)):
            model_prediction[PREDICTION[i]] = float(model_result[i])
        print("MODEL RESULT", list(model_result))
        print("MODEL PREDICTION", model_prediction)

        obj = UserEmotion(timestamp=timezone.now(), emotions=res, prediction=model_prediction)
        obj.save()
        res["pk"] = obj.pk
        res["complex-emotion"] = model_prediction

        return Response(res)     


# send pk to record response later
class ChangeDetect(APIView):
    def post(self, request):
        '''
        RETURNS res object
        '''
        res = UserKeyword.objects.all().order_by('-timestamp')[:ALL_LIM]

        # Min 3 Max 5 after Min 10 in history_all
        
        CUR_LIM = min(max(2, len(res) - MIN_ALL_LIM), JUST_LIM)
        
        print(CUR_LIM, len(res))


        # maps a url to its json keywords
        history_all = dict()
        for obj in res[CUR_LIM:]:
            history_all[obj.url] = json.loads(obj.keywords)
       
        history_just = dict()
        for obj in res[:CUR_LIM]:
            history_just[obj.url] = json.loads(obj.keywords)

        try:
            current_keywords = services.api.getKeywords(request.data.get("url"))
            history_just[request.data.get("url")] = current_keywords
        except Exception as e:
            print(f"Exception in get_keywords: {e}")
            return Response({'error': "Could not get keywords."}, status = status.HTTP_400_BAD_REQUEST)

        with open(FILE_PATH, "r+") as f:
            data = f.read()
            if data == '':
                data = 0        # CP++
            data = int(data)
            f.seek(0)
            f.write(str(data - 1))
            f.truncate()

        if len(res) < MIN_ALL_LIM  or data > 0:
            # Not Enough Data
            print("Not Enough Data") 
            change_detected = False
        else:
            change_detected = services.api.detect_change(history_all=history_all, history_just=history_just)
            print("HISTORY ALL")
            print(history_all, len(history_all))
            print("HISTORY JUST")
            print(history_just, len(history_just))

        new_obj = UserKeyword(timestamp=timezone.now(), keywords=json.dumps(current_keywords), url=request.data.get("url"), prediction=change_detected)
        new_obj.save()
 
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
        
        if response == "Yes":
            # Delete last JUST_LIM from UserKeyword
            pass
        else:
            # Pause the Change Detect Until next JUST_LIM tab openings
            f = open(FILE_PATH, 'w')
            f.write(str(JUST_LIM + 1))
            f.close()

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
        "url": --
    }
],
"user-emotions": [
    {
        "timestamp": --,
        "simple-emotions": {"additional_properties": {}, "anger": 0.0, "contempt": 0.0, "disgust": 0.0, "fear": 0.0, "happiness": 1.0, "neutral": 0.0, "sadness": 0.0, "surprise": 0.0},
        "complex-emotions": {tired: , non_vigilant: , alert: }
    }
]
}
'''

def get_analysis_data(request):
    try:
        cur_date = timezone.now()
        prev_date = cur_date - datetime.timedelta(days=1)
        
        res = {
            "user-keywords": [],
            "user-emotions": []
        }
        
        # get user keywords
        objs1 = UserKeyword.objects.filter(timestamp__range=[prev_date, cur_date]).order_by('timestamp')
        for obj in objs1:
            res["user-keywords"].append({
                "timestamp": str(obj.timestamp),
                "context-switch": obj.response,
                "url": str(obj.url)
            })

        # get user emotions
        objs2 = UserEmotion.objects.filter(timestamp__range=[prev_date, cur_date]).order_by('timestamp')
        for obj in objs2:
            res["user-emotions"].append({
                "timestamp": str(obj.timestamp),
                "simple-emotions": obj.emotions["emotion"],
                "complex-emotions": obj.prediction
            })

        print("ANALYSIS RESULT")
        print(res)
        return HttpResponse(json.dumps(res))
    except Exception as e:
        print(e)
        return HttpResponse("FAIL")
