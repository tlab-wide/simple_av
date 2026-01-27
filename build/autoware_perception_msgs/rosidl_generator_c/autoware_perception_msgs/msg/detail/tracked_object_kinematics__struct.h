// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from autoware_perception_msgs:msg/TrackedObjectKinematics.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_KINEMATICS__STRUCT_H_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_KINEMATICS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Constant 'UNAVAILABLE'.
enum
{
  autoware_perception_msgs__msg__TrackedObjectKinematics__UNAVAILABLE = 0
};

/// Constant 'SIGN_UNKNOWN'.
/**
  * The orientation is determined only up to a sign flip. For instance, assume that cars are
  * longer than they are wide, and the perception pipeline can accurately estimate the
  * dimensions of a car. It should set the orientation to coincide with the major axis, with
  * the sign chosen arbitrarily, and use this tag to signify that the orientation could
  * point to the front or the back.
 */
enum
{
  autoware_perception_msgs__msg__TrackedObjectKinematics__SIGN_UNKNOWN = 1
};

/// Constant 'AVAILABLE'.
/**
  * The full orientation is available. Use e.g. for machine-learning models that can
  * differentiate between the front and back of a vehicle.
 */
enum
{
  autoware_perception_msgs__msg__TrackedObjectKinematics__AVAILABLE = 2
};

// Include directives for member types
// Member 'pose_with_covariance'
#include "geometry_msgs/msg/detail/pose_with_covariance__struct.h"
// Member 'twist_with_covariance'
#include "geometry_msgs/msg/detail/twist_with_covariance__struct.h"
// Member 'acceleration_with_covariance'
#include "geometry_msgs/msg/detail/accel_with_covariance__struct.h"

/// Struct defined in msg/TrackedObjectKinematics in the package autoware_perception_msgs.
/**
  * Only position is available, orientation is empty. Note that the shape can be an oriented
  * bounding box but the direction the object is facing is unknown, in which case
  * orientation should be empty.
 */
typedef struct autoware_perception_msgs__msg__TrackedObjectKinematics
{
  geometry_msgs__msg__PoseWithCovariance pose_with_covariance;
  geometry_msgs__msg__TwistWithCovariance twist_with_covariance;
  geometry_msgs__msg__AccelWithCovariance acceleration_with_covariance;
  uint8_t orientation_availability;
  bool is_stationary;
} autoware_perception_msgs__msg__TrackedObjectKinematics;

// Struct for a sequence of autoware_perception_msgs__msg__TrackedObjectKinematics.
typedef struct autoware_perception_msgs__msg__TrackedObjectKinematics__Sequence
{
  autoware_perception_msgs__msg__TrackedObjectKinematics * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} autoware_perception_msgs__msg__TrackedObjectKinematics__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRACKED_OBJECT_KINEMATICS__STRUCT_H_
