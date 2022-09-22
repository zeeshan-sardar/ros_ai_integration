# Integration of AI Models with ROS

## Overview
The purpose of this repositiry is to integrate a wide range of docker containerized AI models into ROS so that they can run with other robot specific ROS nodes.  

This is not advised to use separate hardware units for robot and AI models. In order to use a single unit for both the AI models and robot, this intgeration plays a vital role. 

The main hardware components we have in our robot are as follows
- [Azure Kinect](https://azure.microsoft.com/en-us/services/kinect-dk/#overview)
- [RPLidar A2](https://www.slamtec.com/en/Lidar/A2)
- [Jetson Xavier NX](https://developer.nvidia.com/embedded/jetson-xavier-nx-devkit)
- Android Tablet
- Microphone and speakers

In this integration architecture, ROS Melodic is running on host OS (Ubuntu 18.04) and every containerized AI model is loaded/unloaded inside a ROS node. This ROS node takes sensor stream from a respectice ROS topic and pass it to the container via a Flask bridge. The same node also gets the model output and publishes it to the desired ROS topic. The visual illustration of the architecture can be seen below.


![alt text](architecture.jpg)

## Technologies
This is built on below technologies
- Nvidia jetson Jetpack 4.6 with Ubuntu 18.04 [(install guide)](https://developer.nvidia.com/embedded/jetpack) 
- ROS Melodic [(install guide)](http://wiki.ros.org/melodic/Installation/Ubuntu) 
- k4a SDK for Azure Kinect [(install guide)](https://github.com/microsoft/Azure_Kinect_ROS_Driver/blob/melodic/docs/building.md) 

## Setup

The third-party libraries are added as submodules along with other developed ROS packages.  
Before cloning this repository, first setup the ROS workspace and src folders.  
```
mkdir catkin_ws #can be a different name
cd catkin_ws
mkdir src
```

After creating workspace, go to src directory of workspace and clone the repository along with submodules (note the dot `.` at the end of the command).
```
cd catkin_ws/src
git clone --recurse-submodules https://github.com/zeeshan-sardar/ros_ai_integration.git .
```

Go back to workspace home directory, install dependencies and build it.
```
cd catkin_ws
rosdep install --from-paths src --ignore-src -r -y
catkin_make
```

## Usage
Instructions are given [here](./ros_ai/scripts/README.md) to run a containerized person tracking model with ROS and Azure Kinect.
