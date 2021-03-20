import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person


# MODULE VARIABLES
OK_FACE_LANDMARKS = False
FACE_ATTR = ['emotion']
API_PARAMS = dict(detection_model='detection_01', 
        return_face_id=True, 
        return_face_landmarks=OK_FACE_LANDMARKS, 
        return_face_attributes=FACE_ATTR, 
        recognition_model='recognition_04')


# LOAD ENV VARIABLES 
# Create your own .env file and add SUBS_KEY & ENDPOINT
import os
from dotenv import load_dotenv
load_dotenv()

KEY = os.getenv("SUBS_KEY")
ENDPOINT = os.getenv("ENDPOINT")


# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))