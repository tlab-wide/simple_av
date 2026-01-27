// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/PlanningWaypoint.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_WAYPOINT__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_WAYPOINT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'waypoint'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/PlanningWaypoint in the package simple_av_msgs.
typedef struct simple_av_msgs__msg__PlanningWaypoint
{
  /// Point with x, y, z coordinates
  geometry_msgs__msg__Point waypoint;
  /// Curve associated with the waypoint
  float curve;
} simple_av_msgs__msg__PlanningWaypoint;

// Struct for a sequence of simple_av_msgs__msg__PlanningWaypoint.
typedef struct simple_av_msgs__msg__PlanningWaypoint__Sequence
{
  simple_av_msgs__msg__PlanningWaypoint * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__PlanningWaypoint__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_WAYPOINT__STRUCT_H_
