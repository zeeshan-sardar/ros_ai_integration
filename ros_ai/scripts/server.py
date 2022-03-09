from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2
import base64
import os

app = Flask(__name__)

@app.route("/edge_detection", methods=['POST'])
def edge_detection():

  data = request.get_json()
  img = np.frombuffer(base64.binascii.a2b_base64(data['img'].encode("ascii")), np.uint8).reshape(480, 640, 3)
  print('image in server:', img.shape)

  img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)

  edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200)

  point = np.array([1,2,3])




  print(edges.shape)
  status = 200
  messege = "-"

  response = {'messege': messege, 'edges': edges, 'point': point, 'status': status}
  response_pickled = jsonpickle.encode(response)

  return Response(response=response_pickled, status=200, mimetype="application/json")

if __name__ == '__main__':

  
  app.run(debug=True, host='0.0.0.0', port=5003, threaded=False)