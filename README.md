# DCCA-Turtlebot3
### DCCA stands for : Depth Camera Collision Avoidance,  
> Gathering useful information for collision avoidance for Autonomous Mobile Robot via only depth camera  
> * undergraduate project from [Human Machine Systems Lab](https://faculty.korea.ac.kr/kufaculty/drsspark/index.do?_ga=2.78727380.1149191488.1646993403-1356205118.1641265679), Korea University

## This repository is based on:
* AMR : [Turtlebot3-burger](https://www.robotis.us/turtlebot-3-burger-us/)
* Depth Camera : [Intel Realsense D435](https://www.intelrealsense.com/depth-camera-d435/)
* MCU : [Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)
* OS : [Jetpack 4.6.1](https://developer.nvidia.com/embedded/downloads)
* Object Detection : [yolov5](https://github.com/ultralytics/yolov5) (pytorch)
* metaOS : ros-melodic (trivial)


## This repository would yield:
* shell script for building the development environment
* RGBDRealsenseCamera : basic camera module that can be broadly used for every realsense camera that has rgb and depth frame in it
* DCCACamera : integrating realsense sdk with yolov5, and automatically formulate [DCCADataStructure](https://github.com/skykongkong8/DCCA-Turtlebot3/blob/main/workspace/dcca_dataStructure/DCCADataStructure.py), which can be useful for motion planning for collision avoidance
* [DCCADataStructure](https://github.com/skykongkong8/DCCA-Turtlebot3/blob/main/workspace/dcca_dataStructure/DCCADataStructure.py) : sample dataStructure based on yolov5 coco dataset 
