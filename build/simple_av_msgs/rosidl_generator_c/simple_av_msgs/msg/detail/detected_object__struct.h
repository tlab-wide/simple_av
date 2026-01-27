// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/DetectedObject.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'position'
// Member 'bounding_box'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'orientation'
#include "geometry_msgs/msg/detail/quaternion__struct.h"
// Member 'shape'
#include "geometry_msgs/msg/detail/vector3__struct.h"
// Member 'relative_direction'
#include "std_msgs/msg/detail/string__struct.h"

/// Struct defined in msg/DetectedObject in the package simple_av_msgs.
/**
  * Whether the data is from RSU (true) or vehicle-mounted sensors (false)
 */
typedef struct simple_av_msgs__msg__DetectedObject
{
  bool is_from_rsu;
  /// Detected object label
  int32_t label;
  /// relative Position of the detected object
  geometry_msgs__msg__Point position;
  /// Object liniear speed
  double velocity;
  /// Orientation of the detected object
  geometry_msgs__msg__Quaternion orientation;
  /// Shape of the detected object (dimensions: x, y, z)
  geometry_msgs__msg__Vector3 shape;
  /// Direction of the object (above, behind, left, right)
  std_msgs__msg__String relative_direction;
  /// x,y positions of 4 side of the vehicle
  geometry_msgs__msg__Point bounding_box[4];
  /// relative distance of the vehicle with the detected object
  double distance;
  /// closest side of the bounding box
  int32_t nearest_object_side;
} simple_av_msgs__msg__DetectedObject;

// Struct for a sequence of simple_av_msgs__msg__DetectedObject.
typedef struct simple_av_msgs__msg__DetectedObject__Sequence
{
  simple_av_msgs__msg__DetectedObject * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__DetectedObject__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__STRUCT_H_
