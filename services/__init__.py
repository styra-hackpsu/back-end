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
from nltk.stem.snowball import SnowballStemmer

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

TEXT_KEY = os.getenv("TEXT_KEY")
TEXT_ENDPOINT = os.getenv("TEXT_ENDPOINT")


# Yake API Details
YAKE = "http://yake.inesctec.pt/yake/v2/extract_keywords_by_url?url=" 
DETAILS = "&max_ngram_size=1&number_of_keywords=20&highlight=false"

# Create stemmer object
stemmer = SnowballStemmer("english")

# Threshold for similarity in history
THRESHOLD = 0.1

# Create an authenticated FaceClient.
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
