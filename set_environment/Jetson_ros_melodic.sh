#<Jetson Nano ubuntu 18.0.04>

sudo apt-get update -y

sudo apt-get upgrade -y

sudo apt-get install -y chrony ntpdate build-essential curl nano

sudo ntpdate ntp.ubuntu.com

sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

sudo apt-get update -y

sudo apt-get install -y ros-melodic-ros-base

sudo apt install python-rosdep

sudo rosdep init

rosdep update

mkdir -p ~/catkin_ws/src

cd ~/catkin_ws/src

sudo apt install ros-melodic-rosserial-python ros-melodic-tf ros-melodic-hls-lfcd-lds-driver

source /opt/ros/melodic/setup.sh

cd ~/catkin_ws && catkin_make

source ~/.bashrc


