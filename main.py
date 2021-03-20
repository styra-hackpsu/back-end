# To cross check module: services

import services.api
import json

# For images hosted
face_image_url = 'https://image.shutterstock.com/image-photo/two-friends-smiling-outside-260nw-371956567.jpg'
face = services.api.face_detect(face_image_url, False)
print(json.loads(face)['emotion']['happiness'])

# # For images as a stream
# face_image = open('./services/sample_data/img.jpg', 'rb')
# face = services.api.face_detect(face_image, True)