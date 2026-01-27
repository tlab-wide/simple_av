// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeTree.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__STRUCT_H_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'nodes'
#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__struct.h"

/// Struct defined in msg/ProcessingTimeTree in the package autoware_internal_debug_msgs.
/**
  * Array of all time nodes
 */
typedef struct autoware_internal_debug_msgs__msg__ProcessingTimeTree
{
  autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence nodes;
} autoware_internal_debug_msgs__msg__ProcessingTimeTree;

// Struct for a sequence of autoware_internal_debug_msgs__msg__ProcessingTimeTree.
typedef struct autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence
{
  autoware_internal_debug_msgs__msg__ProcessingTimeTree * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__STRUCT_H_
