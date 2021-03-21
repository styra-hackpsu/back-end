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

history_all = {"https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string": {'html': 13.377571775537332, 're.compil': 7.931069821737402, 'cleanr': 7.638658684152984, 'beautifulsoup': 7.150060432030654, 'raw': 6.2533801666645425, 'regex': 5.9687415578579115, 'python': 5.469028979774896, 'string': 5.469028979774896, 'lxml': 5.035679307740498, 'cleantext': 4.877462483519439, 'import': 4.315587577883214, 'code': 4.2833682300386995, 'remov': 4.2833682300386995, 'tag': 4.2833682300386995, 'text': 3.2865131627065503, 'addit': 3.191900402657913, 'recommend': 3.1858122295861317, 're.sub': 2.8529457157061935, 'nsbm': 2.8529457157061935, 'insid': 2.286767858129301}}
history_just = {"https://stackoverflow.com/questions/30975339/slicing-a-python-ordereddict": {'getitem': 23.991831983268394, 'slicableordereddict': 17.781199485223254, 'ordereddict': 17.45159440499576, 'python': 13.78113116185656, 'print': 12.192173058752527}}

print(services.api.detect_change(history_all, history_just))
