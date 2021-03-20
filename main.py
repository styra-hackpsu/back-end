# To cross check module: services

import services.api
import json

# For images hosted
face_image_url = 'https://s3.amazonaws.com/s3.mp-cdn.net/12/ce/901b8f87a0314b4f593f0c33597d-is-obama-just-a-really-sad-person.jpg'
face = services.api.face_detect(face_image_url, False)
print(json.dumps(face['emotion']))

# # For images as a stream
# face_image = open('./services/sample_data/img.jpg', 'rb')
# face = services.api.face_detect(face_image, True)