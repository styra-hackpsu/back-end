from services import *
import json
import requests

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

'''
Returns 20 most important keywords for given link 
''' 
def getKeywords(link):
   
    total_keywords = {}
    keywords = json.loads(requests.get(YAKE+link+DETAILS).text)
    keywords = keywords['keywords']
    for word in keywords:
        word['ngram'] = stemmer.stem(word['ngram'])
        
        # Testing
        
        word['score'] = 1/word['score']
        
        # Testing
        
        if word['ngram'] in totol_keywords:
            totol_keywords[word['ngram']] += word['score']
        else:
            totol_keywords[word['ngram']] = word['score']
    
    total_keywords = {k: v for k, v in sorted(totol_keywords.items(), key=lambda item: item[1], reverse=True)}
    
    return total_keywords 


def detect_change(history_all: list, history_just: list) -> bool:

    def getFullHistoryKeyword(history, count):

        top_count = {}
        
        for key in total_keywords.keys():
            top_count[key] = total_keywords[key]
            
            if len(top_count) == count:
                break
        return top_count
    
    keywords_all = getFullHistoryKeyword(history_all, 20)
    keywords_just = getFullHistoryKeyword(history_just, 5)

    count = 0
    total = 0
    for topic in keywords_just:
        if topic in keywords_all:
            print(topic)
            count+=keywords_just[topic]
        total += keywords_just[topic]

    score = count/total
    
    return score > THRESHOLD
