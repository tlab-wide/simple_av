// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/PlanningPathPlanningMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'look_ahead_point'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/PlanningPathPlanningMsg in the package simple_av_msgs.
typedef struct simple_av_msgs__msg__PlanningPathPlanningMsg
{
  geometry_msgs__msg__Point look_ahead_point;
  double speed_limit;
} simple_av_msgs__msg__PlanningPathPlanningMsg;

// Struct for a sequence of simple_av_msgs__msg__PlanningPathPlanningMsg.
typedef struct simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence
{
  simple_av_msgs__msg__PlanningPathPlanningMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__STRUCT_H_
