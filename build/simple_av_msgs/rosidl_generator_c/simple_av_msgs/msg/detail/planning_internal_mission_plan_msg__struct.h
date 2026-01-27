// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/PlanningInternalMissionPlanMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'path'
#include "simple_av_msgs/msg/detail/planning_waypoint__struct.h"
// Member 'path_as_lanes'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/PlanningInternalMissionPlanMsg in the package simple_av_msgs.
typedef struct simple_av_msgs__msg__PlanningInternalMissionPlanMsg
{
  simple_av_msgs__msg__PlanningWaypoint__Sequence path;
  /// Lanes
  rosidl_runtime_c__String__Sequence path_as_lanes;
} simple_av_msgs__msg__PlanningInternalMissionPlanMsg;

// Struct for a sequence of simple_av_msgs__msg__PlanningInternalMissionPlanMsg.
typedef struct simple_av_msgs__msg__PlanningInternalMissionPlanMsg__Sequence
{
  simple_av_msgs__msg__PlanningInternalMissionPlanMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__PlanningInternalMissionPlanMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__STRUCT_H_
