from services import *
import json


def face_detect(face_image: str, is_local: bool) -> dict:
    '''
    Params:
        is_local: Boolean to denote wether image is available locally or hosted
        face_image: path of image
    Desc:
    Returns face parameters and emotions
    Need to use detection model 01 for recognising emotions 
    '''
    if not is_local:
        detected_faces = face_client.face.detect_with_url(url=face_image, **API_PARAMS) 
    else:
        detected_faces = face_client.face.detect_with_stream(image=face_image, **API_PARAMS)

    if not detected_faces:
        raise Exception('No face detected from image {}'.format(face_image))

    res = {
        "id": None,
        "rectangle": None,
        "emotion": None
    }

    # Detected faces are in descending order of their face bounding boxes
    for face in detected_faces: 
        res["id"] = face.face_id
        res["rectangle"] = json.loads(str(face.face_rectangle).replace("\'", "\""))
        res["emotion"] = json.loads(str(face.face_attributes.emotion).replace("\'", "\""))        
        break

    return res
