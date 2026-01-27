// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_internal_metric_msgs:msg/MetricArray.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__STRUCT_H_
#define AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'metric_array'
#include "autoware_internal_metric_msgs/msg/detail/metric__struct.h"

/// Struct defined in msg/MetricArray in the package autoware_internal_metric_msgs.
/**
  * time stamp
 */
typedef struct autoware_internal_metric_msgs__msg__MetricArray
{
  builtin_interfaces__msg__Time stamp;
  /// metrics list
  autoware_internal_metric_msgs__msg__Metric__Sequence metric_array;
} autoware_internal_metric_msgs__msg__MetricArray;

// Struct for a sequence of autoware_internal_metric_msgs__msg__MetricArray.
typedef struct autoware_internal_metric_msgs__msg__MetricArray__Sequence
{
  autoware_internal_metric_msgs__msg__MetricArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_internal_metric_msgs__msg__MetricArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__STRUCT_H_
