// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_map_msgs:msg/MapProjectorInfo.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_MAP_MSGS__MSG__DETAIL__MAP_PROJECTOR_INFO__STRUCT_H_
#define AUTOWARE_MAP_MSGS__MSG__DETAIL__MAP_PROJECTOR_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'LOCAL'.
static const char * const autoware_map_msgs__msg__MapProjectorInfo__LOCAL = "Local";

/// Constant 'LOCAL_CARTESIAN_UTM'.
static const char * const autoware_map_msgs__msg__MapProjectorInfo__LOCAL_CARTESIAN_UTM = "LocalCartesianUTM";

/// Constant 'LOCAL_CARTESIAN'.
static const char * const autoware_map_msgs__msg__MapProjectorInfo__LOCAL_CARTESIAN = "LocalCartesian";

/// Constant 'MGRS'.
static const char * const autoware_map_msgs__msg__MapProjectorInfo__MGRS = "MGRS";

/// Constant 'TRANSVERSE_MERCATOR'.
static const char * const autoware_map_msgs__msg__MapProjectorInfo__TRANSVERSE_MERCATOR = "TransverseMercator";

/// Constant 'WGS84'.
/**
  * Vertical datum
 */
static const char * const autoware_map_msgs__msg__MapProjectorInfo__WGS84 = "WGS84";

/// Constant 'EGM2008'.
static const char * const autoware_map_msgs__msg__MapProjectorInfo__EGM2008 = "EGM2008";

// Include directives for member types
// Member 'projector_type'
// Member 'vertical_datum'
// Member 'mgrs_grid'
#include "rosidl_runtime_c/string.h"
// Member 'map_origin'
#include "geographic_msgs/msg/detail/geo_point__struct.h"

/// Struct defined in msg/MapProjectorInfo in the package autoware_map_msgs.
/**
  * Projector type
 */
typedef struct autoware_map_msgs__msg__MapProjectorInfo
{
  rosidl_runtime_c__String projector_type;
  rosidl_runtime_c__String vertical_datum;
  /// Used for MGRS map
  rosidl_runtime_c__String mgrs_grid;
  /// Used for some map projection types
  /// Altitude is not used, so there is no need to specify it.
  /// Even if altitude is specified, it will be overwritten with 0.0.
  geographic_msgs__msg__GeoPoint map_origin;
  /// Scale factor of the map
  /// Used for TransverseMercator map (default: 0.9996)
  /// In the case of LocalCartesianUTM and MGRS, it will be overwritten with 0.9996.
  /// In the case of Local and LocalCartesian, it will be overwritten with 1.0.
  float scale_factor;
} autoware_map_msgs__msg__MapProjectorInfo;

// Struct for a sequence of autoware_map_msgs__msg__MapProjectorInfo.
typedef struct autoware_map_msgs__msg__MapProjectorInfo__Sequence
{
  autoware_map_msgs__msg__MapProjectorInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_map_msgs__msg__MapProjectorInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_MAP_MSGS__MSG__DETAIL__MAP_PROJECTOR_INFO__STRUCT_H_
