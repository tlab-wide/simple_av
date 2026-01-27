// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from autoware_internal_debug_msgs:msg/Float64MultiArrayStamped.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "autoware_internal_debug_msgs/msg/detail/float64_multi_array_stamped__rosidl_typesupport_introspection_c.h"
#include "autoware_internal_debug_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "autoware_internal_debug_msgs/msg/detail/float64_multi_array_stamped__functions.h"
#include "autoware_internal_debug_msgs/msg/detail/float64_multi_array_stamped__struct.h"


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/time.h"
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__rosidl_typesupport_introspection_c.h"
// Member `layout`
#include "std_msgs/msg/multi_array_layout.h"
// Member `layout`
#include "std_msgs/msg/detail/multi_array_layout__rosidl_typesupport_introspection_c.h"
// Member `data`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__init(message_memory);
}

void autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_fini_function(void * message_memory)
{
  autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__fini(message_memory);
}

size_t autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__size_function__Float64MultiArrayStamped__data(
  const void * untyped_member)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return member->size;
}

const void * autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__get_const_function__Float64MultiArrayStamped__data(
  const void * untyped_member, size_t index)
{
  const rosidl_runtime_c__double__Sequence * member =
    (const rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void * autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__get_function__Float64MultiArrayStamped__data(
  void * untyped_member, size_t index)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  return &member->data[index];
}

void autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__fetch_function__Float64MultiArrayStamped__data(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const double * item =
    ((const double *)
    autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__get_const_function__Float64MultiArrayStamped__data(untyped_member, index));
  double * value =
    (double *)(untyped_value);
  *value = *item;
}

void autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__assign_function__Float64MultiArrayStamped__data(
  void * untyped_member, size_t index, const void * untyped_value)
{
  double * item =
    ((double *)
    autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__get_function__Float64MultiArrayStamped__data(untyped_member, index));
  const double * value =
    (const double *)(untyped_value);
  *item = *value;
}

bool autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__resize_function__Float64MultiArrayStamped__data(
  void * untyped_member, size_t size)
{
  rosidl_runtime_c__double__Sequence * member =
    (rosidl_runtime_c__double__Sequence *)(untyped_member);
  rosidl_runtime_c__double__Sequence__fini(member);
  return rosidl_runtime_c__double__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_member_array[3] = {
  {
    "stamp",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(autoware_internal_debug_msgs__msg__Float64MultiArrayStamped, stamp),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "layout",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(autoware_internal_debug_msgs__msg__Float64MultiArrayStamped, layout),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "data",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(autoware_internal_debug_msgs__msg__Float64MultiArrayStamped, data),  // bytes offset in struct
    NULL,  // default value
    autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__size_function__Float64MultiArrayStamped__data,  // size() function pointer
    autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__get_const_function__Float64MultiArrayStamped__data,  // get_const(index) function pointer
    autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__get_function__Float64MultiArrayStamped__data,  // get(index) function pointer
    autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__fetch_function__Float64MultiArrayStamped__data,  // fetch(index, &value) function pointer
    autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__assign_function__Float64MultiArrayStamped__data,  // assign(index, value) function pointer
    autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__resize_function__Float64MultiArrayStamped__data  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_members = {
  "autoware_internal_debug_msgs__msg",  // message namespace
  "Float64MultiArrayStamped",  // message name
  3,  // number of fields
  sizeof(autoware_internal_debug_msgs__msg__Float64MultiArrayStamped),
  autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_member_array,  // message members
  autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_init_function,  // function to initialize message memory (memory has to be allocated)
  autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_type_support_handle = {
  0,
  &autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_autoware_internal_debug_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, autoware_internal_debug_msgs, msg, Float64MultiArrayStamped)() {
  autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, builtin_interfaces, msg, Time)();
  autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_member_array[1].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, MultiArrayLayout)();
  if (!autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_type_support_handle.typesupport_identifier) {
    autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &autoware_internal_debug_msgs__msg__Float64MultiArrayStamped__rosidl_typesupport_introspection_c__Float64MultiArrayStamped_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
