# DCCA-Turtlebot3
### DCCA stands for : Depth Camera Collision Avoidance,  
> Gathering useful information for collision avoidance for Autonomous Mobile Robot via **ONLY** depth camera  
> * undergraduate project from [Human Machine Systems Lab](https://faculty.korea.ac.kr/kufaculty/drsspark/index.do?_ga=2.78727380.1149191488.1646993403-1356205118.1641265679), Korea University


## This repository is based on:
* AMR : [Turtlebot3-burger](https://www.robotis.us/turtlebot-3-burger-us/)
* Depth Camera : [Intel Realsense D435](https://www.intelrealsense.com/depth-camera-d435/)
* MCU : [Jetson Nano](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)
* OS : [Jetpack 4.6.1](https://developer.nvidia.com/embedded/downloads)
* Object Detection : [yolov5](https://github.com/ultralytics/yolov5) (pytorch)
* metaOS : ros-melodic (trivial)


## This repository would yield something like:
* [set_environment](https://github.com/skykongkong8/DCCA-Turtlebot3/tree/main/set_environment): shell script for building the development environment
* [RGBDRealsenseCamera](https://github.com/skykongkong8/DCCA-Turtlebot3/blob/main/workspace/dcca_camera/RGBDRealsenseCamera.py): basic camera module that can be broadly used for every realsense camera that has rgb and depth frame in it
* [DCCAFilterManager](https://github.com/skykongkong8/DCCA-Turtlebot3/blob/main/workspace/dcca_camera/DCCADepthFilterManager.py): managing detailed settings for the input frame data as a preprocessing
* [DCCACamera](https://github.com/skykongkong8/DCCA-Turtlebot3/blob/main/workspace/dcca_camera/DCCACamera.py): real-time object detection and distancing
* [dcca_relay](https://github.com/skykongkong8/DCCA-Turtlebot3/blob/main/workspace/dcca_relay.py): sample data formulation using gathered data
* various sample codes from pyrealsense2 sdk


## DCCA flow scenario (original intention)
1. Get RGB and Depth frame as input
2. Apply object detection on RGB frame
3. Apply clustering algorithm on Depth frame in the same region w.r.t. detected region from RGB frame, and obtain distance
4. Formulate sample data using detected label and obtained distance

## How to use
1. clone this repository
```git
git clone https://github.com/skykongkong8/DCCA-Turtlebot3.git
```
2. go to workspace directory
```bash
cd DCCA-Turtlebot3/workspace
```
3. run dcca_relay.py
```bash
python3 dcca_relay.py
```
> * caution: if you want to use other modules, you might subtly change importing paths of this repository after cloning...

## TODO
1. adapt into ros-melodic
* issue: opencv4 vs ros1 -> solve by: [do it without opencv4](https://www.youtube.com/watch?v=dB0Sijo0RLs)
2. conjugate with motion planning

### Trivial Error Handling Notes
> This section is about every trivial error that I encountered during the development of this repository, so you may skip here!
1. installing sci-kit learn on Jetson nano  
`sudo apt-get install scikit-learn`
> do NOT use pip
2. almost always use waitKey(t) function while streaming via opencv
3. realsense cameras return depth values with NaN values, so be aware (especially when you are trying to handle them with opencv, Matrix in cpp)  
`Unrecognized or unsupported array type in function ‘cvGetMat’`
4. 
