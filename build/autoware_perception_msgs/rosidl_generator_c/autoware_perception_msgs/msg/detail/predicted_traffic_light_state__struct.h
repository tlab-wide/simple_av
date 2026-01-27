// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_perception_msgs:msg/PredictedTrafficLightState.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__STRUCT_H_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'INFORMATION_SOURCE_V2N'.
static const char * const autoware_perception_msgs__msg__PredictedTrafficLightState__INFORMATION_SOURCE_V2N = "V2N";

/// Constant 'INFORMATION_SOURCE_V2I'.
static const char * const autoware_perception_msgs__msg__PredictedTrafficLightState__INFORMATION_SOURCE_V2I = "V2I";

/// Constant 'INFORMATION_SOURCE_V2V'.
static const char * const autoware_perception_msgs__msg__PredictedTrafficLightState__INFORMATION_SOURCE_V2V = "V2V";

/// Constant 'INFORMATION_SOURCE_LOCAL_PERCEPTION'.
static const char * const autoware_perception_msgs__msg__PredictedTrafficLightState__INFORMATION_SOURCE_LOCAL_PERCEPTION = "LOCAL_PERCEPTION";

/// Constant 'INFORMATION_SOURCE_MANUAL_OVERRIDE'.
static const char * const autoware_perception_msgs__msg__PredictedTrafficLightState__INFORMATION_SOURCE_MANUAL_OVERRIDE = "MANUAL_OVERRIDE";

/// Constant 'INFORMATION_SOURCE_SIMULATION'.
static const char * const autoware_perception_msgs__msg__PredictedTrafficLightState__INFORMATION_SOURCE_SIMULATION = "SIMULATION";

/// Constant 'INFORMATION_SOURCE_INTERNAL_ESTIMATION'.
static const char * const autoware_perception_msgs__msg__PredictedTrafficLightState__INFORMATION_SOURCE_INTERNAL_ESTIMATION = "INTERNAL_ESTIMATION";

// Include directives for member types
// Member 'predicted_stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'simultaneous_elements'
#include "autoware_perception_msgs/msg/detail/traffic_light_element__struct.h"
// Member 'information_source'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/PredictedTrafficLightState in the package autoware_perception_msgs.
/**
  * Information source values (string constants):
  * - V2N: Signal data sent from a server (Internet)
  * - V2I: Direct from RSU (Roadside Unit)
  * - V2V: Signal data from another vehicle
  * - LOCAL_PERCEPTION: Information detected by onboard sensors
  * - MANUAL_OVERRIDE: Manually set signal data (for testing/debugging)
  * - SIMULATION: Signal data from a simulated environment
  * - INTERNAL_ESTIMATION: Information that was predicted by an onboard model
 */
typedef struct autoware_perception_msgs__msg__PredictedTrafficLightState
{
  /// Absolute time this state is expected
  builtin_interfaces__msg__Time predicted_stamp;
  /// Valid signals at this time
  autoware_perception_msgs__msg__TrafficLightElement__Sequence simultaneous_elements;
  /// Confidence level
  float reliability;
  /// Source of information, using predefined string constants
  rosidl_runtime_c__String information_source;
} autoware_perception_msgs__msg__PredictedTrafficLightState;

// Struct for a sequence of autoware_perception_msgs__msg__PredictedTrafficLightState.
typedef struct autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence
{
  autoware_perception_msgs__msg__PredictedTrafficLightState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__STRUCT_H_
