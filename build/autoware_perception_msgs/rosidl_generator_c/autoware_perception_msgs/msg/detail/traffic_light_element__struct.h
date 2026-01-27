// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_perception_msgs:msg/TrafficLightElement.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_ELEMENT__STRUCT_H_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_ELEMENT__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'UNKNOWN'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__UNKNOWN = 0
};

/// Constant 'RED'.
/**
  * constants for color
 */
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__RED = 1
};

/// Constant 'AMBER'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__AMBER = 2
};

/// Constant 'GREEN'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__GREEN = 3
};

/// Constant 'WHITE'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__WHITE = 4
};

/// Constant 'CIRCLE'.
/**
  * constants for shape
 */
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__CIRCLE = 1
};

/// Constant 'LEFT_ARROW'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__LEFT_ARROW = 2
};

/// Constant 'RIGHT_ARROW'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__RIGHT_ARROW = 3
};

/// Constant 'UP_ARROW'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__UP_ARROW = 4
};

/// Constant 'UP_LEFT_ARROW'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__UP_LEFT_ARROW = 5
};

/// Constant 'UP_RIGHT_ARROW'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__UP_RIGHT_ARROW = 6
};

/// Constant 'DOWN_ARROW'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__DOWN_ARROW = 7
};

/// Constant 'DOWN_LEFT_ARROW'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__DOWN_LEFT_ARROW = 8
};

/// Constant 'DOWN_RIGHT_ARROW'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__DOWN_RIGHT_ARROW = 9
};

/// Constant 'CROSS'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__CROSS = 10
};

/// Constant 'SOLID_OFF'.
/**
  * constants for status
 */
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__SOLID_OFF = 1
};

/// Constant 'SOLID_ON'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__SOLID_ON = 2
};

/// Constant 'FLASHING'.
enum
{
  autoware_perception_msgs__msg__TrafficLightElement__FLASHING = 3
};

/// Struct defined in msg/TrafficLightElement in the package autoware_perception_msgs.
/**
  * constants for common use
 */
typedef struct autoware_perception_msgs__msg__TrafficLightElement
{
  /// variables
  uint8_t color;
  uint8_t shape;
  uint8_t status;
  float confidence;
} autoware_perception_msgs__msg__TrafficLightElement;

// Struct for a sequence of autoware_perception_msgs__msg__TrafficLightElement.
typedef struct autoware_perception_msgs__msg__TrafficLightElement__Sequence
{
  autoware_perception_msgs__msg__TrafficLightElement * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_perception_msgs__msg__TrafficLightElement__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_ELEMENT__STRUCT_H_
