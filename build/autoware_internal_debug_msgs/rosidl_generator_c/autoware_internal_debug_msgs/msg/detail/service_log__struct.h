// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_internal_debug_msgs:msg/ServiceLog.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__SERVICE_LOG__STRUCT_H_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__SERVICE_LOG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'CLIENT_REQUEST'.
enum
{
  autoware_internal_debug_msgs__msg__ServiceLog__CLIENT_REQUEST = 1
};

/// Constant 'SERVER_REQUEST'.
enum
{
  autoware_internal_debug_msgs__msg__ServiceLog__SERVER_REQUEST = 2
};

/// Constant 'SERVER_RESPONSE'.
enum
{
  autoware_internal_debug_msgs__msg__ServiceLog__SERVER_RESPONSE = 3
};

/// Constant 'CLIENT_RESPONSE'.
enum
{
  autoware_internal_debug_msgs__msg__ServiceLog__CLIENT_RESPONSE = 4
};

/// Constant 'ERROR_UNREADY'.
enum
{
  autoware_internal_debug_msgs__msg__ServiceLog__ERROR_UNREADY = 5
};

/// Constant 'ERROR_TIMEOUT'.
enum
{
  autoware_internal_debug_msgs__msg__ServiceLog__ERROR_TIMEOUT = 6
};

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'name'
// Member 'node'
// Member 'yaml'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/ServiceLog in the package autoware_internal_debug_msgs.
typedef struct autoware_internal_debug_msgs__msg__ServiceLog
{
  builtin_interfaces__msg__Time stamp;
  uint8_t type;
  rosidl_runtime_c__String name;
  rosidl_runtime_c__String node;
  rosidl_runtime_c__String yaml;
} autoware_internal_debug_msgs__msg__ServiceLog;

// Struct for a sequence of autoware_internal_debug_msgs__msg__ServiceLog.
typedef struct autoware_internal_debug_msgs__msg__ServiceLog__Sequence
{
  autoware_internal_debug_msgs__msg__ServiceLog * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_internal_debug_msgs__msg__ServiceLog__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__SERVICE_LOG__STRUCT_H_
