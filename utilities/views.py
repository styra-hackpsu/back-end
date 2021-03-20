from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions

import services.api
from .models import UserEmotion, UserKeyword
from .serializers import UserEmotionSerializer, UserKeywordSerializer

# Create your views here.
def index(request):
    return Response({"status": "Services are up & running!"})


class FaceDetect(APIView):
    def post(self, request):
        return Response(services.api.face_detect(request.data.get("path"), request.data.get("choice")))        


class UserEmotionViewSet(viewsets.ModelViewSet):
    queryset = UserEmotion.objects.all().order_by('timestamp')
    serializer_class = UserEmotionSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserKeywordViewSet(viewsets.ModelViewSet):
    queryset = UserKeyword.objects.all().order_by('timestamp')
    serializer_class = UserKeywordSerializer
    permission_classes = [permissions.IsAuthenticated]
