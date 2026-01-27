// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/PlanningMotionPlanningMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'stop_point'
#include "geometry_msgs/msg/detail/point__struct.h"
// Member 'status'
// Member 'stop_reason'
#include "std_msgs/msg/detail/string__struct.h"

/// Struct defined in msg/PlanningMotionPlanningMsg in the package simple_av_msgs.
typedef struct simple_av_msgs__msg__PlanningMotionPlanningMsg
{
  geometry_msgs__msg__Point stop_point;
  std_msgs__msg__String status;
  std_msgs__msg__String stop_reason;
} simple_av_msgs__msg__PlanningMotionPlanningMsg;

// Struct for a sequence of simple_av_msgs__msg__PlanningMotionPlanningMsg.
typedef struct simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence
{
  simple_av_msgs__msg__PlanningMotionPlanningMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__STRUCT_H_
