// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from autoware_map_msgs:msg/LaneletMapCellMetaData.idl
// generated code does not contain a copyright notice
#include "autoware_map_msgs/msg/detail/lanelet_map_cell_meta_data__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "autoware_map_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "autoware_map_msgs/msg/detail/lanelet_map_cell_meta_data__struct.h"
#include "autoware_map_msgs/msg/detail/lanelet_map_cell_meta_data__functions.h"
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

#include "rosidl_runtime_c/string.h"  // cell_id
#include "rosidl_runtime_c/string_functions.h"  // cell_id

// forward declare type support functions


using _LaneletMapCellMetaData__ros_msg_type = autoware_map_msgs__msg__LaneletMapCellMetaData;

static bool _LaneletMapCellMetaData__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _LaneletMapCellMetaData__ros_msg_type * ros_message = static_cast<const _LaneletMapCellMetaData__ros_msg_type *>(untyped_ros_message);
  // Field name: cell_id
  {
    const rosidl_runtime_c__String * str = &ros_message->cell_id;
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

  // Field name: min_x
  {
    cdr << ros_message->min_x;
  }

  // Field name: max_x
  {
    cdr << ros_message->max_x;
  }

  // Field name: min_y
  {
    cdr << ros_message->min_y;
  }

  // Field name: max_y
  {
    cdr << ros_message->max_y;
  }

  return true;
}

static bool _LaneletMapCellMetaData__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _LaneletMapCellMetaData__ros_msg_type * ros_message = static_cast<_LaneletMapCellMetaData__ros_msg_type *>(untyped_ros_message);
  // Field name: cell_id
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->cell_id.data) {
      rosidl_runtime_c__String__init(&ros_message->cell_id);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->cell_id,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'cell_id'\n");
      return false;
    }
  }

  // Field name: min_x
  {
    cdr >> ros_message->min_x;
  }

  // Field name: max_x
  {
    cdr >> ros_message->max_x;
  }

  // Field name: min_y
  {
    cdr >> ros_message->min_y;
  }

  // Field name: max_y
  {
    cdr >> ros_message->max_y;
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_autoware_map_msgs
size_t get_serialized_size_autoware_map_msgs__msg__LaneletMapCellMetaData(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _LaneletMapCellMetaData__ros_msg_type * ros_message = static_cast<const _LaneletMapCellMetaData__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name cell_id
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->cell_id.size + 1);
  // field.name min_x
  {
    size_t item_size = sizeof(ros_message->min_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name max_x
  {
    size_t item_size = sizeof(ros_message->max_x);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name min_y
  {
    size_t item_size = sizeof(ros_message->min_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name max_y
  {
    size_t item_size = sizeof(ros_message->max_y);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _LaneletMapCellMetaData__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_autoware_map_msgs__msg__LaneletMapCellMetaData(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_autoware_map_msgs
size_t max_serialized_size_autoware_map_msgs__msg__LaneletMapCellMetaData(
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

  // member: cell_id
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
  // member: min_x
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: max_x
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: min_y
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: max_y
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint64_t);
    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = autoware_map_msgs__msg__LaneletMapCellMetaData;
    is_plain =
      (
      offsetof(DataType, max_y) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _LaneletMapCellMetaData__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_autoware_map_msgs__msg__LaneletMapCellMetaData(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_LaneletMapCellMetaData = {
  "autoware_map_msgs::msg",
  "LaneletMapCellMetaData",
  _LaneletMapCellMetaData__cdr_serialize,
  _LaneletMapCellMetaData__cdr_deserialize,
  _LaneletMapCellMetaData__get_serialized_size,
  _LaneletMapCellMetaData__max_serialized_size
};

static rosidl_message_type_support_t _LaneletMapCellMetaData__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_LaneletMapCellMetaData,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, autoware_map_msgs, msg, LaneletMapCellMetaData)() {
  return &_LaneletMapCellMetaData__type_support;
}

#if defined(__cplusplus)
}
#endif
