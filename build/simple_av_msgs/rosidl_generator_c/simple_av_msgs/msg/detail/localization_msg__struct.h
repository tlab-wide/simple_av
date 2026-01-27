// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/LocalizationMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'closest_point'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'closest_lane_names'
#include "std_msgs/msg/detail/string__struct.h"

/// Struct defined in msg/LocalizationMsg in the package simple_av_msgs.
typedef struct simple_av_msgs__msg__LocalizationMsg
{
  geometry_msgs__msg__Point closest_point;
  std_msgs__msg__String closest_lane_names;
  double minimal_distance;
} simple_av_msgs__msg__LocalizationMsg;

// Struct for a sequence of simple_av_msgs__msg__LocalizationMsg.
typedef struct simple_av_msgs__msg__LocalizationMsg__Sequence
{
  simple_av_msgs__msg__LocalizationMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__LocalizationMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__STRUCT_H_
