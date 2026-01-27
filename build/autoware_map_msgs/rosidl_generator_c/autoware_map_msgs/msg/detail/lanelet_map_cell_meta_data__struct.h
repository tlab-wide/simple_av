// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_map_msgs:msg/LaneletMapCellMetaData.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_CELL_META_DATA__STRUCT_H_
#define AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_CELL_META_DATA__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'cell_id'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/LaneletMapCellMetaData in the package autoware_map_msgs.
/**
  * Metadata of lanelet map cell
 */
typedef struct autoware_map_msgs__msg__LaneletMapCellMetaData
{
  rosidl_runtime_c__String cell_id;
  double min_x;
  double max_x;
  double min_y;
  double max_y;
} autoware_map_msgs__msg__LaneletMapCellMetaData;

// Struct for a sequence of autoware_map_msgs__msg__LaneletMapCellMetaData.
typedef struct autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence
{
  autoware_map_msgs__msg__LaneletMapCellMetaData * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_CELL_META_DATA__STRUCT_H_
