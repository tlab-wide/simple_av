// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_map_msgs:srv/GetSelectedLanelet2Map.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_MAP_MSGS__SRV__DETAIL__GET_SELECTED_LANELET2_MAP__STRUCT_H_
#define AUTOWARE_MAP_MSGS__SRV__DETAIL__GET_SELECTED_LANELET2_MAP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'cell_ids'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/GetSelectedLanelet2Map in the package autoware_map_msgs.
typedef struct autoware_map_msgs__srv__GetSelectedLanelet2Map_Request
{
  rosidl_runtime_c__String__Sequence cell_ids;
} autoware_map_msgs__srv__GetSelectedLanelet2Map_Request;

// Struct for a sequence of autoware_map_msgs__srv__GetSelectedLanelet2Map_Request.
typedef struct autoware_map_msgs__srv__GetSelectedLanelet2Map_Request__Sequence
{
  autoware_map_msgs__srv__GetSelectedLanelet2Map_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_map_msgs__srv__GetSelectedLanelet2Map_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'lanelet2_cells'
#include "autoware_map_msgs/msg/detail/lanelet_map_bin__struct.h"

/// Struct defined in srv/GetSelectedLanelet2Map in the package autoware_map_msgs.
typedef struct autoware_map_msgs__srv__GetSelectedLanelet2Map_Response
{
  std_msgs__msg__Header header;
  /// Newly loaded Lanelet map
  autoware_map_msgs__msg__LaneletMapBin lanelet2_cells;
} autoware_map_msgs__srv__GetSelectedLanelet2Map_Response;

// Struct for a sequence of autoware_map_msgs__srv__GetSelectedLanelet2Map_Response.
typedef struct autoware_map_msgs__srv__GetSelectedLanelet2Map_Response__Sequence
{
  autoware_map_msgs__srv__GetSelectedLanelet2Map_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_map_msgs__srv__GetSelectedLanelet2Map_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_MAP_MSGS__SRV__DETAIL__GET_SELECTED_LANELET2_MAP__STRUCT_H_
