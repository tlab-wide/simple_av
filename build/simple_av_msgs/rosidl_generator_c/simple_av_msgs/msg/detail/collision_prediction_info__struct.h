// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/CollisionPredictionInfo.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'object_position'
#include "geometry_msgs/msg/detail/point__struct.h"

/// Struct defined in msg/CollisionPredictionInfo in the package simple_av_msgs.
typedef struct simple_av_msgs__msg__CollisionPredictionInfo
{
  geometry_msgs__msg__Point object_position;
  double time_to_collision;
  int32_t object_label;
  double object_velocity;
  bool collision_detected;
} simple_av_msgs__msg__CollisionPredictionInfo;

// Struct for a sequence of simple_av_msgs__msg__CollisionPredictionInfo.
typedef struct simple_av_msgs__msg__CollisionPredictionInfo__Sequence
{
  simple_av_msgs__msg__CollisionPredictionInfo * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__CollisionPredictionInfo__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__STRUCT_H_
