// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeTree.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "autoware_internal_debug_msgs/msg/detail/processing_time_tree__rosidl_typesupport_introspection_c.h"
#include "autoware_internal_debug_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "autoware_internal_debug_msgs/msg/detail/processing_time_tree__functions.h"
#include "autoware_internal_debug_msgs/msg/detail/processing_time_tree__struct.h"


// Include directives for member types
// Member `nodes`
#include "autoware_internal_debug_msgs/msg/processing_time_node.h"
// Member `nodes`
#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__rosidl_typesupport_introspection_c.h"

#ifdef __cplusplus
extern "C"
{
#endif

void autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  autoware_internal_debug_msgs__msg__ProcessingTimeTree__init(message_memory);
}

void autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_fini_function(void * message_memory)
{
  autoware_internal_debug_msgs__msg__ProcessingTimeTree__fini(message_memory);
}

size_t autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__size_function__ProcessingTimeTree__nodes(
  const void * untyped_member)
{
  const autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * member =
    (const autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence *)(untyped_member);
  return member->size;
}

const void * autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__get_const_function__ProcessingTimeTree__nodes(
  const void * untyped_member, size_t index)
{
  const autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * member =
    (const autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence *)(untyped_member);
  return &member->data[index];
}

void * autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__get_function__ProcessingTimeTree__nodes(
  void * untyped_member, size_t index)
{
  autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * member =
    (autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence *)(untyped_member);
  return &member->data[index];
}

void autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__fetch_function__ProcessingTimeTree__nodes(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const autoware_internal_debug_msgs__msg__ProcessingTimeNode * item =
    ((const autoware_internal_debug_msgs__msg__ProcessingTimeNode *)
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__get_const_function__ProcessingTimeTree__nodes(untyped_member, index));
  autoware_internal_debug_msgs__msg__ProcessingTimeNode * value =
    (autoware_internal_debug_msgs__msg__ProcessingTimeNode *)(untyped_value);
  *value = *item;
}

void autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__assign_function__ProcessingTimeTree__nodes(
  void * untyped_member, size_t index, const void * untyped_value)
{
  autoware_internal_debug_msgs__msg__ProcessingTimeNode * item =
    ((autoware_internal_debug_msgs__msg__ProcessingTimeNode *)
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__get_function__ProcessingTimeTree__nodes(untyped_member, index));
  const autoware_internal_debug_msgs__msg__ProcessingTimeNode * value =
    (const autoware_internal_debug_msgs__msg__ProcessingTimeNode *)(untyped_value);
  *item = *value;
}

bool autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__resize_function__ProcessingTimeTree__nodes(
  void * untyped_member, size_t size)
{
  autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * member =
    (autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence *)(untyped_member);
  autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__fini(member);
  return autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__init(member, size);
}

static rosidl_typesupport_introspection_c__MessageMember autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_message_member_array[1] = {
  {
    "nodes",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(autoware_internal_debug_msgs__msg__ProcessingTimeTree, nodes),  // bytes offset in struct
    NULL,  // default value
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__size_function__ProcessingTimeTree__nodes,  // size() function pointer
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__get_const_function__ProcessingTimeTree__nodes,  // get_const(index) function pointer
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__get_function__ProcessingTimeTree__nodes,  // get(index) function pointer
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__fetch_function__ProcessingTimeTree__nodes,  // fetch(index, &value) function pointer
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__assign_function__ProcessingTimeTree__nodes,  // assign(index, value) function pointer
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__resize_function__ProcessingTimeTree__nodes  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_message_members = {
  "autoware_internal_debug_msgs__msg",  // message namespace
  "ProcessingTimeTree",  // message name
  1,  // number of fields
  sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeTree),
  autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_message_member_array,  // message members
  autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_init_function,  // function to initialize message memory (memory has to be allocated)
  autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_message_type_support_handle = {
  0,
  &autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_autoware_internal_debug_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, autoware_internal_debug_msgs, msg, ProcessingTimeTree)() {
  autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, autoware_internal_debug_msgs, msg, ProcessingTimeNode)();
  if (!autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_message_type_support_handle.typesupport_identifier) {
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &autoware_internal_debug_msgs__msg__ProcessingTimeTree__rosidl_typesupport_introspection_c__ProcessingTimeTree_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
