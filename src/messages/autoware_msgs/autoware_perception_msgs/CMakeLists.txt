cmake_minimum_required(VERSION 3.14)
project(autoware_perception_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Dependencies used inside the .msg files
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(unique_identifier_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/DetectedObject.msg"
  "msg/DetectedObjectKinematics.msg"
  "msg/DetectedObjects.msg"
  "msg/ObjectClassification.msg"
  "msg/PredictedObject.msg"
  "msg/PredictedObjectKinematics.msg"
  "msg/PredictedObjects.msg"
  "msg/PredictedPath.msg"
  "msg/PredictedTrafficLightState.msg"
  "msg/Shape.msg"
  "msg/TrackedObject.msg"
  "msg/TrackedObjectKinematics.msg"
  "msg/TrackedObjects.msg"
  "msg/TrafficLightElement.msg"
  "msg/TrafficLightGroup.msg"
  "msg/TrafficLightGroupArray.msg"
  "msg/TrafficSignalElement.msg"
  "msg/TrafficSignal.msg"
  "msg/TrafficSignalArray.msg"
  DEPENDENCIES
    std_msgs
    geometry_msgs
    builtin_interfaces
    unique_identifier_msgs
)

ament_export_dependencies(rosidl_default_runtime)

ament_package()
