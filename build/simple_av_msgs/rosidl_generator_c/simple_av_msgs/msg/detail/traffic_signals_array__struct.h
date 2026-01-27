// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/TrafficSignalsArray.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'v2i_traffic_signals_id'
// Member 'v2i_traffic_signals_colors'
#include "rosidl_runtime_c/primitives_sequence.h"

/// Struct defined in msg/TrafficSignalsArray in the package simple_av_msgs.
/**
  * List of traffic signal IDs
 */
typedef struct simple_av_msgs__msg__TrafficSignalsArray
{
  rosidl_runtime_c__int32__Sequence v2i_traffic_signals_id;
  /// List of corresponding traffic signal colors
  rosidl_runtime_c__int32__Sequence v2i_traffic_signals_colors;
} simple_av_msgs__msg__TrafficSignalsArray;

// Struct for a sequence of simple_av_msgs__msg__TrafficSignalsArray.
typedef struct simple_av_msgs__msg__TrafficSignalsArray__Sequence
{
  simple_av_msgs__msg__TrafficSignalsArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__TrafficSignalsArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__STRUCT_H_
