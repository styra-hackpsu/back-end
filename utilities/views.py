from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import services.api

# Create your views here.
def index(request):
    return HttpResponse("Services are up & running!")

@csrf_exempt
def face_detect(request):
    assert (request.method == 'POST')
    print(request.POST.get("name"))
    # return HttpResponse(str(services.api.face_detect(path, choice)))
    return HttpResponse(":(")