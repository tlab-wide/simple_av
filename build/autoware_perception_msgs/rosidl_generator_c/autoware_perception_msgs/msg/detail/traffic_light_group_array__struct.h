// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_perception_msgs:msg/TrafficLightGroupArray.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP_ARRAY__STRUCT_H_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'traffic_light_groups'
#include "autoware_perception_msgs/msg/detail/traffic_light_group__struct.h"

/// Struct defined in msg/TrafficLightGroupArray in the package autoware_perception_msgs.
typedef struct autoware_perception_msgs__msg__TrafficLightGroupArray
{
  builtin_interfaces__msg__Time stamp;
  autoware_perception_msgs__msg__TrafficLightGroup__Sequence traffic_light_groups;
} autoware_perception_msgs__msg__TrafficLightGroupArray;

// Struct for a sequence of autoware_perception_msgs__msg__TrafficLightGroupArray.
typedef struct autoware_perception_msgs__msg__TrafficLightGroupArray__Sequence
{
  autoware_perception_msgs__msg__TrafficLightGroupArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_perception_msgs__msg__TrafficLightGroupArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP_ARRAY__STRUCT_H_
