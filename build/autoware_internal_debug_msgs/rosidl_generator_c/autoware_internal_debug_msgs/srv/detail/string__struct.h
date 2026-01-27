// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_internal_debug_msgs:srv/String.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__STRUCT_H_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'data'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/String in the package autoware_internal_debug_msgs.
typedef struct autoware_internal_debug_msgs__srv__String_Request
{
  rosidl_runtime_c__String data;
} autoware_internal_debug_msgs__srv__String_Request;

// Struct for a sequence of autoware_internal_debug_msgs__srv__String_Request.
typedef struct autoware_internal_debug_msgs__srv__String_Request__Sequence
{
  autoware_internal_debug_msgs__srv__String_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_internal_debug_msgs__srv__String_Request__Sequence;


// Constants defined in the message

/// Struct defined in srv/String in the package autoware_internal_debug_msgs.
typedef struct autoware_internal_debug_msgs__srv__String_Response
{
  bool success;
} autoware_internal_debug_msgs__srv__String_Response;

// Struct for a sequence of autoware_internal_debug_msgs__srv__String_Response.
typedef struct autoware_internal_debug_msgs__srv__String_Response__Sequence
{
  autoware_internal_debug_msgs__srv__String_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_internal_debug_msgs__srv__String_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__STRUCT_H_
