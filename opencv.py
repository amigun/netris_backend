import time

import cv2
import json
import random
import string

from ai import prediction, model
from redis_db import set_classes

cls_old = list()
classes = [
    'kran',
    'ekskavator',
    'traktor',
    'gruz'
]


def write2json(filename, cls_new: list[str]):
    global cls_old

    for cl in classes:
        if cls_new.count(cl) > cls_old.count(cl):
            print('new')
            for i in range(cls_new.count(cl) - cls_old.count(cl)):
                with open(f'uploads/{filename}.json', 'r') as f:
                    json_file = json.load(f)

                json_file.append(
                    {
                        'id': ''.join([random.choice(string.ascii_letters + string.digits) for j in range(16)]),
                        'class': cl,
                        'timestamp_start': str(int(time.time())),
                        'timestamp_end': ''
                    }
                )

                with open(f'uploads/{filename}.json', 'w') as f:
                    json.dump(json_file, f, indent=4)

        elif cls_new.count(cl) < cls_old.count(cl):
            print('minus')
            for i in range(cls_old.count(cl) - cls_new.count(cl)):
                with open(f'uploads/{filename}.json', 'r') as f:
                    json_file = json.load(f)

                for event in json_file:
                    if event.get('class') == cl and event.get('timestamp_end') == '':
                        new_event = event
                        new_event['timestamp_end'] = str(int(time.time()))
                        json_file[json_file.index(event)] = new_event

                        with open(f'uploads/{filename}.json', 'w') as f:
                            json.dump(json_file, f, indent=4)

    cls_old = cls_new


def get_frames(filename):
    capture = cv2.VideoCapture(f'uploads/{filename}')

    while capture.isOpened():
        success, frame = capture.read()

        if not success:
            break
        else:
            predict = prediction(frame)

            clist = predict[0].boxes.cls
            cls_new = list()

            for cno in clist:
                cls_new.append(model.names[int(cno)])

            write2json(filename, cls_new)
            set_classes(
                filename,
                str(int(time.time())),
                cls_new
            )

            annotated_frame = predict[0].plot()

            ret, buffer = cv2.imencode('.jpg', annotated_frame)

            frame = buffer.tobytes()

            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
