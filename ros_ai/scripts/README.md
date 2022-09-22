# Launching the Person Tracking Model with ROS

The setup details are given [here](../../README.md).

Use the following instructions to launch the model and respective ROS node.

1. After setting up Azure Kinect, launch the node   
`roslaunch azure_kinect_ros_driver kinect_rgbd.launch`
2. Run the server inside the docker container of person tracking model  
`sudo docker run --runtime=nvidia --network=host --mount type=bind,source="$(pwd)"/Data,target=/app/Data smartpetdocker/smartpet:fr_person_tracking_api`
3. In the end, launch the client ROS node   
`rosrun ros_ai int_ros_ai2.py`

