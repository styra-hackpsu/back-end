from services import *
import json


def face_detect(face_image_url: str) -> dict:
    '''
    Params:
        face_image_url: (Needs hosting)
    Desc:
    Returns face parameters and emotions
    Need to use detection model 01 for recognising emotions 
    '''
    image_name = os.path.basename(face_image_url)
    
    detected_faces = face_client.face.detect_with_url(url=face_image_url, 
        detection_model='detection_01', 
        return_face_id=True, 
        return_face_landmarks=OK_FACE_LANDMARKS, 
        return_face_attributes=FACE_ATTR, 
        recognition_model='recognition_04')

    if not detected_faces:
        raise Exception('No face detected from image {}'.format(image_name))

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
