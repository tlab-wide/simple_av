// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_internal_metric_msgs:msg/Metric.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__STRUCT_H_
#define AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'name'
// Member 'unit'
// Member 'value'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Metric in the package autoware_internal_metric_msgs.
/**
  * name of the metric
 */
typedef struct autoware_internal_metric_msgs__msg__Metric
{
  rosidl_runtime_c__String name;
  /// unit (or type) of the metric
  /// you can leave it empty or assign any identifier to the unit, such as "milliseconds", "m/s", "IoU", "battery percentage", etc.
  rosidl_runtime_c__String unit;
  /// value of the metric
  rosidl_runtime_c__String value;
} autoware_internal_metric_msgs__msg__Metric;

// Struct for a sequence of autoware_internal_metric_msgs__msg__Metric.
typedef struct autoware_internal_metric_msgs__msg__Metric__Sequence
{
  autoware_internal_metric_msgs__msg__Metric * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_internal_metric_msgs__msg__Metric__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__STRUCT_H_
