#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from geometry_msgs.msg import PointStamped
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import PointCloud2
import ros_numpy


# import k4a
# import docker
import base64
import time
import requests
import json
import numpy as np
import cv2

class integration:

    def __init__(self):

        print('inside init')
        self.bridge = CvBridge()

        self.addr = 'http://localhost:5000'
        self.test_url =  self.addr + '/track_person'

        # prepare headers for http request
        self.content_type = 'application/json'
        self.headers = {'content-type': self.content_type}
        
        self.data = ''

        self.xyz_image = None
        self.cv_image = None

        self.point = PointStamped()


       
        '''
        Setting up docker clinet and running the container
        '''
        # self.client = docker.from_env()
        # container = self.client.containers.run("ros_ai_int_simple:latest", remove=True, network_mode='host', detach=True, 
        # volumes=['/home/zeeshan/xavor/int_ws/src/ros_ai/scripts:/app'])

        # container = self.client.containers.run("ros_ai_int_simple:latest", remove=True, network_mode='host', detach=True)
        
        rospy.init_node('integration', anonymous=True)
    

        self.pub = rospy.Publisher('/person_loc', PointStamped, queue_size=10)
        rospy.Subscriber("/rgb/image_rect_color", Image, self.img_callback)
        rospy.Subscriber("/points2", PointCloud2, self.pc_callback)

    def pc_callback(self, pc2_msg):
  
        try:
            pc = ros_numpy.point_cloud2.pointcloud2_to_xyz_array(pc2_msg, remove_nans=False)
            
        except CvBridgeError as e:
            print(e)
            
        if pc is not None:
            # print('PC shape:', pc.shape)
            pc_x = pc[:,0].reshape((720, 1280))
            pc_y = pc[:,1].reshape((720, 1280))
            pc_z = pc[:,2].reshape((720, 1280))

            # print('PC center point raw:', np.stack([pc_x,pc_y, pc_z], axis=2)[360,640,:])
            xyz_image = np.stack([pc_x,pc_y, pc_z], axis=2)
            self.xyz_image = (xyz_image*1000).astype(np.int16)
            # print('PC center point float16:', self.xyz_image[360,640,:])

            # print(self.xyz_image.shape)


    def img_callback(self, data):

        try:
            self.cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)


    def run(self):

        # rate = rospy.Rate(4)

        while  not rospy.is_shutdown():
            if self.cv_image is not None and self.xyz_image is not None:
                string_img = base64.binascii.b2a_base64(self.cv_image).decode("ascii")
                str_point_cloud = base64.binascii.b2a_base64(self.xyz_image).decode("ascii") 
            
                self.data = {'image': string_img, "image_shape": self.cv_image.shape, 'point_cloud': str_point_cloud, 'point_cloud_shape': self.xyz_image.shape}

                t0 = time.time()
                response = requests.post(self.test_url, json=self.data, headers=self.headers)
                print("Inference time: " + str(time.time() - t0))
                

                response = json.loads(response.text)
                # response_decoded = jsonpickle.decode(response['point'])
                point = response['point']

                self.point.header.stamp = rospy.Time.now()
                self.point.header.frame_id = 'azure_link'

                if point is None:
                    self.point.point.x = -9999
                    self.point.point.y = -9999
                    self.point.point.z = -9999
                else:
                    self.point.point.x = point[0]
                    self.point.point.y = point[1]
                    self.point.point.z = point[2]

                rospy.loginfo(response)

                self.pub.publish( self.point)

                # window_name = 'image'
                # cv2.imshow(window_name, self.xyz_image.astype('uint16'))
                # cv2.waitKey(0) 
                # cv2.destroyAllWindows() 

            # rate.sleep()



if __name__ == '__main__':
    try:
        inter = integration()
        inter.run()

    except rospy.ROSInterruptException:
        pass

