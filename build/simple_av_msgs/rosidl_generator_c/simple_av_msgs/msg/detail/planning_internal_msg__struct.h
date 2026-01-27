// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/PlanningInternalMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/PlanningInternalMsg in the package simple_av_msgs.
/**
  * msg from path planner to motion planner
 */
typedef struct simple_av_msgs__msg__PlanningInternalMsg
{
  bool is_curve_detected;
  bool is_end_of_path;
} simple_av_msgs__msg__PlanningInternalMsg;

// Struct for a sequence of simple_av_msgs__msg__PlanningInternalMsg.
typedef struct simple_av_msgs__msg__PlanningInternalMsg__Sequence
{
  simple_av_msgs__msg__PlanningInternalMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__PlanningInternalMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__STRUCT_H_
