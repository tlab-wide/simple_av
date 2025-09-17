#!/bin/bash
sudo apt update
sudo apt install -y ros-humble-lanelet2 ros-humble-lanelet2-extension
sudo apt install -y ros-humble-lanelet2-projection ros-humble-lanelet2-routing ros-humble-lanelet2-traffic-rules ros-humble-lanelet2-maps
# sudo apt install -y ros-humble-lanelet2 ros-humble-lanelet2-extension
sudo apt install ros-humble-lanelet2 ros-humble-lanelet2-io
sudo apt install -y ros-humble-geographic-msgs
sudo apt install -y librange-v3-dev
sudo apt install -y libtinyxml2-dev ros-humble-tinyxml2-vendor