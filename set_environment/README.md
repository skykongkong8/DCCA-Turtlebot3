# set_environment
Device : Jetson Nano (Jetpack 4.6.1, ubuntu 18.0.4)
All files in this repository is about building development environment for the following:
> Recommendation: open and observe the each command whenever you encounter unexpected error, and restart from there.

1. how_to_setup.txt
* commands for setting Jetson Nano with turtlebot3 (OpenCR1.0, dynamixel sdk, ros-melodic)

2. Jetson_ros_melodic.sh
* shell script for installing ros-melodic on Jetson Nano

3. yolov5dependencies_opencv4_pytorch18_torchvision090.sh
* shell script for installing and configuring all the requirements for yolov5 objectdetection on Jetson Nano which are:
    * opencv4
    * pytorch1.8
    * torchvision0.9.0