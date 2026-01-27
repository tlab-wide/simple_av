// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/SimMonitor.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/SimMonitor in the package simple_av_msgs.
typedef struct simple_av_msgs__msg__SimMonitor
{
  double system_time;
  double sim_time;
  /// sim_time/system_time
  double sim_clock_rate;
} simple_av_msgs__msg__SimMonitor;

// Struct for a sequence of simple_av_msgs__msg__SimMonitor.
typedef struct simple_av_msgs__msg__SimMonitor__Sequence
{
  simple_av_msgs__msg__SimMonitor * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__SimMonitor__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__STRUCT_H_
