# To cross check module: services

import services.api
import json

face_image_url = 'https://image.shutterstock.com/image-photo/two-friends-smiling-outside-260nw-371956567.jpg'
face = services.api.face_detect(face_image_url)

print(face['emotion']['anger'])