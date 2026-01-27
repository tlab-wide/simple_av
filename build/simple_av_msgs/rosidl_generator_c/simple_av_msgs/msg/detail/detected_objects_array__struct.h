// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/DetectedObjectsArray.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECTS_ARRAY__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECTS_ARRAY__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'objects'
#include "simple_av_msgs/msg/detail/detected_object__struct.h"

/// Struct defined in msg/DetectedObjectsArray in the package simple_av_msgs.
/**
  * Array of detected objects
 */
typedef struct simple_av_msgs__msg__DetectedObjectsArray
{
  simple_av_msgs__msg__DetectedObject__Sequence objects;
} simple_av_msgs__msg__DetectedObjectsArray;

// Struct for a sequence of simple_av_msgs__msg__DetectedObjectsArray.
typedef struct simple_av_msgs__msg__DetectedObjectsArray__Sequence
{
  simple_av_msgs__msg__DetectedObjectsArray * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__DetectedObjectsArray__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECTS_ARRAY__STRUCT_H_
