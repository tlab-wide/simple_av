// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/LocalizationIntersectionStatus.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'intersection_name'
// Member 'status'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/LocalizationIntersectionStatus in the package simple_av_msgs.
/**
  * Name of the intersection (e.g., "1", "2")
 */
typedef struct simple_av_msgs__msg__LocalizationIntersectionStatus
{
  rosidl_runtime_c__String intersection_name;
  /// Status can be: "approaching", "in", "exiting", or "none"
  rosidl_runtime_c__String status;
  /// Distance (in meters) from the vehicle to the intersection point
  float distance_to_intersection;
} simple_av_msgs__msg__LocalizationIntersectionStatus;

// Struct for a sequence of simple_av_msgs__msg__LocalizationIntersectionStatus.
typedef struct simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence
{
  simple_av_msgs__msg__LocalizationIntersectionStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__STRUCT_H_
