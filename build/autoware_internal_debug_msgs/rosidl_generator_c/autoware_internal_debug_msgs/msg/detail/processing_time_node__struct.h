// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeNode.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_NODE__STRUCT_H_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_NODE__STRUCT_H_

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
// Member 'comment'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ProcessingTimeNode in the package autoware_internal_debug_msgs.
/**
  * Unique ID of the node
 */
typedef struct autoware_internal_debug_msgs__msg__ProcessingTimeNode
{
  int32_t id;
  /// Name of the node
  rosidl_runtime_c__String name;
  /// Processing time of the node
  double processing_time;
  /// ID of the parent node, 0 if no parent
  int32_t parent_id;
  /// Comment
  rosidl_runtime_c__String comment;
} autoware_internal_debug_msgs__msg__ProcessingTimeNode;

// Struct for a sequence of autoware_internal_debug_msgs__msg__ProcessingTimeNode.
typedef struct autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence
{
  autoware_internal_debug_msgs__msg__ProcessingTimeNode * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_NODE__STRUCT_H_
