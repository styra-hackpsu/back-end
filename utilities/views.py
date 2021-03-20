from rest_framework.views import APIView
from rest_framework.response import Response

import services.api

# Create your views here.
def index(request):
    return Response({"status": "Services are up & running!"})



class FaceDetect(APIView):
    def post(self, request):
        return Response(services.api.face_detect(request.data.get("path"), request.data.get("choice")))        