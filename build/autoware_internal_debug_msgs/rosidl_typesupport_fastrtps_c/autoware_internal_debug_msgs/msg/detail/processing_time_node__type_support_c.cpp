// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeNode.idl
// generated code does not contain a copyright notice
#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "autoware_internal_debug_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__struct.h"
#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // comment, name
#include "rosidl_runtime_c/string_functions.h"  // comment, name

// forward declare type support functions


using _ProcessingTimeNode__ros_msg_type = autoware_internal_debug_msgs__msg__ProcessingTimeNode;

static bool _ProcessingTimeNode__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _ProcessingTimeNode__ros_msg_type * ros_message = static_cast<const _ProcessingTimeNode__ros_msg_type *>(untyped_ros_message);
  // Field name: id
  {
    cdr << ros_message->id;
  }

  // Field name: name
  {
    const rosidl_runtime_c__String * str = &ros_message->name;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: processing_time
  {
    cdr << ros_message->processing_time;
  }

  // Field name: parent_id
  {
    cdr << ros_message->parent_id;
  }

  // Field name: comment
  {
    const rosidl_runtime_c__String * str = &ros_message->comment;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _ProcessingTimeNode__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _ProcessingTimeNode__ros_msg_type * ros_message = static_cast<_ProcessingTimeNode__ros_msg_type *>(untyped_ros_message);
  // Field name: id
  {
    cdr >> ros_message->id;
  }

  // Field name: name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->name.data) {
      rosidl_runtime_c__String__init(&ros_message->name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'name'\n");
      return false;
    }
  }

  // Field name: processing_time
  {
    cdr >> ros_message->processing_time;
  }

  // Field name: parent_id
  {
    cdr >> ros_message->parent_id;
  }

  // Field name: comment
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->comment.data) {
      rosidl_runtime_c__String__init(&ros_message->comment);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->comment,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'comment'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_autoware_internal_debug_msgs
size_t get_serialized_size_autoware_internal_debug_msgs__msg__ProcessingTimeNode(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _ProcessingTimeNode__ros_msg_type * ros_message = static_cast<const _ProcessingTimeNode__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name id
  {
    size_t item_size = sizeof(ros_message->id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->name.size + 1);
  // field.name processing_time
  {
    size_t item_size = sizeof(ros_message->processing_time);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name parent_id
  {
    size_t item_size = sizeof(ros_message->parent_id);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name comment
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->comment.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _ProcessingTimeNode__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_autoware_internal_debug_msgs__msg__ProcessingTimeNode(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_autoware_internal_debug_msgs
size_t max_serialized_size_autoware_internal_debug_msgs__msg__ProcessingTimeNode(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: name
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: processing_time
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: parent_id
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }
  // member: comment
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = autoware_internal_debug_msgs__msg__ProcessingTimeNode;
    is_plain =
      (
      offsetof(DataType, comment) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _ProcessingTimeNode__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_autoware_internal_debug_msgs__msg__ProcessingTimeNode(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_ProcessingTimeNode = {
  "autoware_internal_debug_msgs::msg",
  "ProcessingTimeNode",
  _ProcessingTimeNode__cdr_serialize,
  _ProcessingTimeNode__cdr_deserialize,
  _ProcessingTimeNode__get_serialized_size,
  _ProcessingTimeNode__max_serialized_size
};

static rosidl_message_type_support_t _ProcessingTimeNode__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_ProcessingTimeNode,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, autoware_internal_debug_msgs, msg, ProcessingTimeNode)() {
  return &_ProcessingTimeNode__type_support;
}

#if defined(__cplusplus)
}
#endif
