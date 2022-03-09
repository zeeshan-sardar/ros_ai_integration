import k4a
import cv2
import json
import numpy
import base64
import requests

import numpy as np
import open3d as o3d

  
addr = 'http://10.21.21.186:5000'
test_url = addr + '/track_person'

# prepare headers for http request
content_type = 'application/json'
headers = {'content-type': content_type}


def main():
	device = k4a.Device.open()
	print("deice opened")
	if device is None:
		print("Failed to open device\n")
		exit(-1)

	device_config = k4a.DeviceConfiguration(
		color_format=k4a.EImageFormat.COLOR_BGRA32,
		color_resolution=k4a.EColorResolution.RES_720P,
		depth_mode=k4a.EDepthMode.NFOV_2X2BINNED,
		camera_fps=k4a.EFramesPerSecond.FPS_30,
		synchronized_images_only=True,
		depth_delay_off_color_usec=0,
		wired_sync_mode=k4a.EWiredSyncMode.STANDALONE,
		subordinate_delay_off_master_usec=0,
		disable_streaming_indicator=False)

	status = device.start_cameras(device_config)
	if status != k4a.EStatus.SUCCEEDED:
		print("Failed to start cameras\n")
		exit(-1)

	# In order to create a Transformation class, we first need to get
	# a Calibration instance. Getting a calibration object needs the
	# depth mode and color camera resolution. Thankfully, this is part
	# of the device configuration used in the start_cameras() function.
	calibration = device.get_calibration(
		depth_mode=device_config.depth_mode,
		color_resolution=device_config.color_resolution)

	# Create a Transformation object using the calibration object as param.
	transform = k4a.Transformation(calibration)

	# pcd = o3d.geometry.PointCloud()

	while True:

		capture = device.get_capture(-1)
		
		color_frame = capture.color
		color_image = color_frame.data
		color_image = numpy.asarray(color_image[:, :, :3], order='C')
		
		depth_frame = capture.depth
		
		depth_frame_transformed = transform.depth_image_to_color_camera(depth_frame) # depth_to_rgb/image_raw
		height, width = depth_frame_transformed.data.shape
		xy_depth = depth_frame_transformed.data.reshape(height * width)
		xyz_image = transform.depth_image_to_point_cloud(depth_frame_transformed, k4a.ECalibrationType.COLOR)

		points = xyz_image.data
		print(color_image.shape, points.shape)
		# pcd.points = o3d.utility.Vector3dVector(points)
		# o3d.visualization.draw_geometries([pcd])

		string_img = base64.binascii.b2a_base64(color_image).decode("ascii")
		str_point_cloud = base64.binascii.b2a_base64(points).decode("ascii") 
		
		data = {'image': string_img, "image_shape": color_image.shape, 'point_cloud': str_point_cloud, 'point_cloud_shape': points.shape}
		
		response = requests.post(test_url, json=data, headers=headers)
		response = json.loads(response.text)
		print(response)

		cv2.namedWindow("SiamMask", cv2.WND_PROP_FULLSCREEN)
		cv2.imshow('SiamMask', color_image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
       

if __name__ == '__main__':
    main()
