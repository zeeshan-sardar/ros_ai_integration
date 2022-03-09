#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import docker
import base64
import time
import requests
import jsonpickle
import json

class integration:

    def __init__(self):

        print('inside init')
        self.bridge = CvBridge()

        self.addr = 'http://localhost:5002'
        self.test_url = self.addr + '/edge_detection'

        # prepare headers for http request
        self.content_type = 'application/json'
        self.headers = {'content-type': self.content_type}
        
        self.data = ''

        self.client = docker.from_env()
        # container = self.client.containers.run("ros_ai_int_simple:latest", remove=True, network_mode='host', detach=True, 
        # volumes=['/home/zeeshan/xavor/int_ws/src/ros_ai/scripts:/app'])

        # container = self.client.containers.run("ros_ai_int_simple:latest", remove=True, network_mode='host', detach=True)
        
        rospy.init_node('integration', anonymous=True)
    

        self.pub = rospy.Publisher('chatter', String, queue_size=10)
        rospy.Subscriber("/camera/image_raw", Image, self.callback)

        rospy.spin()


    def callback(self, data):
        
        # rospy.loginfo(rospy.get_caller_id() + "I heard ")

        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        self.pub.publish(hello_str)

        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        if cv_image is not None:
            print(cv_image.shape)
            string_img = base64.binascii.b2a_base64(cv_image).decode("ascii")
            self.data = {'img': string_img }

            t0 = time.time()
            response = requests.post(self.test_url, json=self.data, headers=self.headers)
            print("Inference time: " + str(time.time() - t0))

            

            response = json.loads(response.text)
            response_decoded = jsonpickle.decode(response['point'])
            print(response_decoded)





if __name__ == '__main__':
    try:
        inter = integration()
    except rospy.ROSInterruptException:
        pass

