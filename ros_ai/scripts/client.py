
from __future__ import print_function
import requests
import json
import jsonpickle
import time
import cv2
import base64
import os
import datetime
# import numpy as np


addr = 'http://localhost:5003'
test_url = addr + '/edge_detection'

# prepare headers for http request
content_type = 'application/json'
headers = {'content-type': content_type}


def static_img():
    img = cv2.imread("2.jpg")
    img = cv2.resize(img, (480, 640))
    print('image read in zeeshan:', img.shape)

    string_img = base64.binascii.b2a_base64(img).decode("ascii")
    data = {'img': string_img }

    t0 = time.time()
    response = requests.post(test_url, json=data, headers=headers)
    print("Inference time: " + str(time.time() - t0))

    response_decoded = jsonpickle.decode(response.text)

    # response_decoded = json.loads(response.text)
    print(response_decoded['edges'])

    cv2.imshow('window_name', response_decoded['edges'])
    cv2.waitKey(0) 
    cv2.destroyAllWindows()  


def live_test(record=False):
    previousResults = [('No Spill Found', None)]
    cap = cv2.VideoCapture(2)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("fps: ", fps)
    i = 0
    if record:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('SD_' + str(datetime.datetime.now()) + '.avi', fourcc, 30.0, (1280, 800))
    while True:
        ret, cv_image = cap.read()
        start = time.time()
        # print("inside")
        if cv_image is not None:
            print("cv_image is not None")
            print(cv_image.shape)
            #### API here ######
            string_img = base64.binascii.b2a_base64(cv_image).decode("ascii")
            data = {'img': string_img}
            t0 = time.time()
            response = requests.post(test_url, json=data, headers=headers)
            print("Inference time: " + str(time.time() - t0))
            response = json.loads(response.text)

            spillage_results = response['class, confidence'], response['boxes']
            #####################
            print(spillage_results[0])
            if spillage_results[0] != "No Spill Found" and previousResults[0] != spillage_results:
                spillage_results_array = spillage_results[0].split(',')
                spillage_class, conf = spillage_results_array[0], spillage_results_array[1]
                # spillage_results[0] = spillage_class
                if spillage_class != "No Spill Found":
                    cv_image = cv2.putText(cv_image, spillage_class + " confidence:" + str(conf), (10, 25),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 255), 2, cv2.LINE_AA)
                    currentTime = datetime.datetime.now().isoformat()
                    path_to_store = "MediaStorage/SD_" + str(currentTime) + '.jpg'
                    cv2.imwrite(path_to_store, cv_image)
                    # break
            previousResults.append(spillage_results[0])
            previousResults.pop(0)
            print(previousResults)

            if record:
                out.write(cv_image)
            cv2.imshow("Image window", cv_image)
            # cv2.waitKey(1)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    if record:
        out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # live_test(record=True)
    static_img()
