from django.http import HttpResponse
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from django.utils import timezone

import math
import json
import datetime
import random

import services.api
import services.emotion_model.model
import services.responses
from .models import UserEmotion, UserKeyword
from .serializers import UserEmotionSerializer, UserKeywordSerializer


# NOTE THE USE OF "None" for features that haven't been recorded

PREDICTION = {0: "alert",  1: "non_vigilant",  2: "tired"}
ORDER_EMOTIONS = ['anger','contempt','disgust','fear','happiness','neutral','sadness','surprise']
ALERT_EMOTIONS = ['anger', 'sadness', 'non_vigilant', 'tired']
# To store singular counts
CHANGE_DETECT_FILE_PATH = './utilities/change_detect_data.txt'
FACE_DETECT_FILE_PATH = './utilities/face_detect_data.txt'
# Emotion Call Count Check
FACE_DETECT_CALL_COUNT = 6
FACE_DETECT_CALL_THRESHOLD = 0.6 
# Segregation between history just and history all
JUST_LIM = 4
ALL_LIM = 24
MIN_ALL_LIM = 10
# Neutral emotion bias
NEUTRAL_BIAS = 3
MODEL_CHECK_THRESHOLD = 0.90


# send pk to record response later
class FaceDetect(APIView):
    def post(self, request):
        '''
            RECORDS res object (See db for sample return under USER EMOTION) (API Call from services/api/face_detect)
            RETURNS fres (with remedy and emotion)
        '''

        try:
            res = services.api.face_detect(request.data.get("path"), request.data.get("choice"))
        except Exception as e:
            print(f"Exception in face_detect: {e}")
            return Response({'error': "Could not detect faces."}, status = status.HTTP_400_BAD_REQUEST)
        
        # Sample API response
        # res = {
        #     "emotion": {
        #         'anger': 0.05,
        #         'contempt': 0.05,
        #         'disgust': 0.05,
        #         'fear': 0.1,
        #         'happiness': 0.05,
        #         'neutral': 0.05,
        #         'sadness': 0.6,
        #         'surprise': 0.05
        #     }
        # }
        
        # TODO: INCLUDE MODEL HERE
        model_input = [0.2, 0.05, 0.05, 0.05, 0.05, 0.05, 0.5, 0.05]
        # model_input = [float(res['emotion'][x]) for x in ORDER_EMOTIONS]
        print("MODEL INPUT", model_input)
        model_result = services.emotion_model.model.predict(model_input)
        model_prediction = dict()
        for i in range(len(model_result)):
            model_prediction[PREDICTION[i]] = float(model_result[i])
        print("MODEL RESULT", list(model_result))
        print("MODEL PREDICTION", model_prediction)

        res["complex-emotion"] = model_prediction
        obj = UserEmotion(timestamp=timezone.now(), emotions=res, prediction=model_prediction)
        obj.save()
        res["pk"] = obj.pk
        


        with open(FACE_DETECT_FILE_PATH, "r+") as f:
            data = f.read()
            if data == '':
                data = 1
            data = int(data)
            f.seek(0)
            f.write(str((data + 1) % FACE_DETECT_CALL_COUNT))
            f.truncate()

        fres = {
            "status": "OK",
            "content": "Entry added to DB",
            "got_emotion": False,
            "timestamp": str(timezone.now())
        }

        print("FACE DETECT DATA COUNT")
        print("DATA", data)
        print("TOTAL COUNT", FACE_DETECT_CALL_COUNT)

        # extract the top emotion
        if data == 0:
            print("FACE DETECT CALL COUNT REACHED")
            objlist = UserEmotion.objects.all().order_by('-timestamp')[:FACE_DETECT_CALL_COUNT]
            rankings = {}
            for x in ORDER_EMOTIONS:
                rankings[x] = 0
            for obj in objlist:
                for cur in obj.emotions["emotion"]:
                    x = obj.emotions["emotion"][cur]
                    if cur == "neutral":
                        x /= NEUTRAL_BIAS
                    rankings[cur] = max(rankings[cur], x)

            # filter from rankings
            for custom_emotion in ORDER_EMOTIONS:
                if custom_emotion not in ALERT_EMOTIONS:
                    rankings.pop(custom_emotion)
                
            major_emotion = sorted(rankings.items(), key=lambda item: item[1], reverse=True)[0]

            print("MAJOR EMOTION", major_emotion)
            fres["got_emotion"] = True
            fres["emotion"] = []
            fres["quote"] = []
            if (major_emotion[1] > FACE_DETECT_CALL_THRESHOLD) and (major_emotion[0] in ALERT_EMOTIONS):
                print("THRESHOLD CAPTURED")
                fres["emotion"].append(major_emotion[0])
                fres["quote"].append(random.choice(services.responses.singled_responses[major_emotion[0]]))
            
            crankings = {}
            for x in list(PREDICTION.values()):
                crankings[x] = 0
            for obj in objlist:
                for cur in obj.emotions["complex-emotion"]:
                    x = obj.emotions["complex-emotion"][cur]
                    crankings[cur] += (x / len(PREDICTION))
            major_cemotion = sorted(crankings.items(), key=lambda item: item[1], reverse=True)[0]
            if (major_cemotion[0] in ALERT_EMOTIONS) and (major_cemotion[1] > FACE_DETECT_CALL_THRESHOLD):
                print("MAJOR COMPLEX EMOTION", major_cemotion)
                fres["emotion"].append(major_cemotion[0])
                fres["quote"].append(random.choice(services.responses.singled_responses[major_cemotion[0]]))
            
            # IF NOT FOUND
            if len(fres["emotion"]) == 0:
                fres["got_emotion"] = False

        print("FINAL RESPONSE")
        print(fres)

        return Response(fres)     


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
            history_all[obj.url] = obj.keywords
       
        history_just = dict()
        for obj in res[:CUR_LIM]:
            history_just[obj.url] = obj.keywords

        try:
            current_keywords = services.api.get_keywords(request.data.get("url"))
            history_just[request.data.get("url")] = current_keywords
        except Exception as e:
            print(f"Exception in get_keywords: {e}")
            return Response({'error': "Could not get keywords."}, status = status.HTTP_400_BAD_REQUEST)

        with open(CHANGE_DETECT_FILE_PATH, "r+") as f:
            data = f.read()
            if data == '':
                data = 0        
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

        new_obj = UserKeyword(timestamp=timezone.now(), keywords=current_keywords, url=request.data.get("url"), prediction=change_detected)
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
            f = open(CHANGE_DETECT_FILE_PATH, 'w')
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
