// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from autoware_internal_metric_msgs:msg/MetricArray.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "autoware_internal_metric_msgs/msg/detail/metric_array__rosidl_typesupport_introspection_c.h"
#include "autoware_internal_metric_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "autoware_internal_metric_msgs/msg/detail/metric_array__functions.h"
#include "autoware_internal_metric_msgs/msg/detail/metric_array__struct.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"
// Member `metric_array`
#include "autoware_internal_metric_msgs/msg/metric.h"
// Member `metric_array`
#include "autoware_internal_metric_msgs/msg/detail/metric__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  autoware_internal_metric_msgs__msg__MetricArray__init(message_memory);
}

void autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_fini_function(void * message_memory)
{
  autoware_internal_metric_msgs__msg__MetricArray__fini(message_memory);
}

size_t autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__size_function__MetricArray__metric_array(
  const void * untyped_member)
{
  const autoware_internal_metric_msgs__msg__Metric__Sequence * member =
    (const autoware_internal_metric_msgs__msg__Metric__Sequence *)(untyped_member);
  return member->size;
}

const void * autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__get_const_function__MetricArray__metric_array(
  const void * untyped_member, size_t index)
{
  const autoware_internal_metric_msgs__msg__Metric__Sequence * member =
    (const autoware_internal_metric_msgs__msg__Metric__Sequence *)(untyped_member);
  return &member->data[index];
}

void * autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__get_function__MetricArray__metric_array(
  void * untyped_member, size_t index)
{
  autoware_internal_metric_msgs__msg__Metric__Sequence * member =
    (autoware_internal_metric_msgs__msg__Metric__Sequence *)(untyped_member);
  return &member->data[index];
}

void autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__fetch_function__MetricArray__metric_array(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const autoware_internal_metric_msgs__msg__Metric * item =
    ((const autoware_internal_metric_msgs__msg__Metric *)
    autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__get_const_function__MetricArray__metric_array(untyped_member, index));
  autoware_internal_metric_msgs__msg__Metric * value =
    (autoware_internal_metric_msgs__msg__Metric *)(untyped_value);
  *value = *item;
}

void autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__assign_function__MetricArray__metric_array(
  void * untyped_member, size_t index, const void * untyped_value)
{
  autoware_internal_metric_msgs__msg__Metric * item =
    ((autoware_internal_metric_msgs__msg__Metric *)
    autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__get_function__MetricArray__metric_array(untyped_member, index));
  const autoware_internal_metric_msgs__msg__Metric * value =
    (const autoware_internal_metric_msgs__msg__Metric *)(untyped_value);
  *item = *value;
}

bool autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__resize_function__MetricArray__metric_array(
  void * untyped_member, size_t size)
{
  autoware_internal_metric_msgs__msg__Metric__Sequence * member =
    (autoware_internal_metric_msgs__msg__Metric__Sequence *)(untyped_member);
  autoware_internal_metric_msgs__msg__Metric__Sequence__fini(member);
  return autoware_internal_metric_msgs__msg__Metric__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_member_array[2] = {
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(autoware_internal_metric_msgs__msg__MetricArray, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "metric_array",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(autoware_internal_metric_msgs__msg__MetricArray, metric_array),  // bytes offset in struct
    NULL,  // default value
    autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__size_function__MetricArray__metric_array,  // size() function pointer
    autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__get_const_function__MetricArray__metric_array,  // get_const(index) function pointer
    autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__get_function__MetricArray__metric_array,  // get(index) function pointer
    autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__fetch_function__MetricArray__metric_array,  // fetch(index, &value) function pointer
    autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__assign_function__MetricArray__metric_array,  // assign(index, value) function pointer
    autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__resize_function__MetricArray__metric_array  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_members = {
  "autoware_internal_metric_msgs__msg",  // message namespace
  "MetricArray",  // message name
  2,  // number of fields
  sizeof(autoware_internal_metric_msgs__msg__MetricArray),
  autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_member_array,  // message members
  autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_init_function,  // function to initialize message memory (memory has to be allocated)
  autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_type_support_handle = {
  0,
  &autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_autoware_internal_metric_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, autoware_internal_metric_msgs, msg, MetricArray)() {
  autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, autoware_internal_metric_msgs, msg, Metric)();
  if (!autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_type_support_handle.typesupport_identifier) {
    autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &autoware_internal_metric_msgs__msg__MetricArray__rosidl_typesupport_introspection_c__MetricArray_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
