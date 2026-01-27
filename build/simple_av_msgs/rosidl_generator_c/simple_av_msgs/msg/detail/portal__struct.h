// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:msg/Portal.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__STRUCT_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/Portal in the package simple_av_msgs.
typedef struct simple_av_msgs__msg__Portal
{
  bool reset;
  int32_t round_number;
  bool finished;
} simple_av_msgs__msg__Portal;

// Struct for a sequence of simple_av_msgs__msg__Portal.
typedef struct simple_av_msgs__msg__Portal__Sequence
{
  simple_av_msgs__msg__Portal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__msg__Portal__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__STRUCT_H_
