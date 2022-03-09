# Launch Azure Kinect node
roslaunch azure_kinect_ros_driver kinect_rgbd.launch 

# Run Object Detection Model
sudo docker run --runtime=nvidia --network=host smartpetdocker/smartpet:fr_person_tracking_api


# Run Integrated Node
rosrun ros_ai int_ros_ai2.py k