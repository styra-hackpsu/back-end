import services.api
from os.path import isfile, join
import os
import time
import pandas as pd


# PARAMS
SLEEP_TIME = 1.2
CLASSES = {"alert": 0, "non_vigilant": 1, "tired": 2}
DIR = "non_vigilant" # TRAINING CLASS
MODE = "test"
OUTFILE = f"./dataset/{DIR}_{MODE}.csv"

# FINAL RESULT
res = {"anger": [], 
    "contempt": [], 
    "disgust": [], 
    "fear": [], 
    "happiness": [], 
    "neutral": [], 
    "sadness": [], 
    "surprise": [],
    "class": []}

PATH = f"./dataset/{MODE}/{DIR}/"
files = [PATH + f for f in os.listdir(PATH) if isfile(join(PATH, f))]

api_lim_reached = False
all_files_read = False
file_ptr = 0
while not (api_lim_reached or all_files_read):
    while file_ptr < len(files):
        img = open(files[file_ptr], 'rb')
        print(f"FILE SIZE for {files[file_ptr]}", os.stat(files[file_ptr]).st_size)
        try:
            face = services.api.face_detect(img, True)
            for feature in face['emotion']:
                try:
                    res[feature].append(face['emotion'][feature])
                except Exception:
                    pass
            res["class"].append(CLASSES[DIR])
        except Exception as e:
            print('Exception', e)
            if str(e) == "API FAIL":
                file_ptr += 1
                continue
            elif str(e) == "API LIMIT":
                print("SLEEP START")
                api_lim_reached = True
                break
        file_ptr += 1
    if api_lim_reached:
        time.sleep(SLEEP_TIME)
        print("SLEEP COMPLETE")
        api_lim_reached = False
    else:
        all_files_read = True
    
df = pd.DataFrame.from_dict(res)
print("CLASS", DIR)
print(df.head())
df.to_csv(OUTFILE, index=False)
