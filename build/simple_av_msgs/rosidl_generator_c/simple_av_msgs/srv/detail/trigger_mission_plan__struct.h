// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from simple_av_msgs:srv/TriggerMissionPlan.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__STRUCT_H_
#define SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in srv/TriggerMissionPlan in the package simple_av_msgs.
typedef struct simple_av_msgs__srv__TriggerMissionPlan_Request
{
  uint8_t structure_needs_at_least_one_member;
} simple_av_msgs__srv__TriggerMissionPlan_Request;

// Struct for a sequence of simple_av_msgs__srv__TriggerMissionPlan_Request.
typedef struct simple_av_msgs__srv__TriggerMissionPlan_Request__Sequence
{
  simple_av_msgs__srv__TriggerMissionPlan_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__srv__TriggerMissionPlan_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/TriggerMissionPlan in the package simple_av_msgs.
typedef struct simple_av_msgs__srv__TriggerMissionPlan_Response
{
  bool success;
  rosidl_runtime_c__String message;
} simple_av_msgs__srv__TriggerMissionPlan_Response;

// Struct for a sequence of simple_av_msgs__srv__TriggerMissionPlan_Response.
typedef struct simple_av_msgs__srv__TriggerMissionPlan_Response__Sequence
{
  simple_av_msgs__srv__TriggerMissionPlan_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} simple_av_msgs__srv__TriggerMissionPlan_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__STRUCT_H_
