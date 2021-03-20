from services import *
import json


def face_detect(face_image: str, is_local: bool) -> json:
    '''
    Params:
        is_local: Boolean to denote wether image is available locally or hosted
        face_image: path of image
    Desc:
    Returns face parameters and emotions
    Need to use detection model 01 for recognising emotions 
    '''

    try:
        if not is_local:
            detected_faces = face_client.face.detect_with_url(url=face_image, **API_PARAMS) 
        else:
            detected_faces = face_client.face.detect_with_stream(image=face_image, **API_PARAMS)
    except Exception as e:
        print("Services Module:", e)
        if (str(e).find('429') != -1):
            raise Exception('API LIMIT')
        else:
            raise Exception('API FAIL')

    if not detected_faces:
        print("Services module: NO FACE DETECTED")
        raise Exception('API FAIL')

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
