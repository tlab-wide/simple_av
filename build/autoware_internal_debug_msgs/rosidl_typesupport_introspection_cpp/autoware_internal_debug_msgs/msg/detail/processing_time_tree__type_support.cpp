// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeTree.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "autoware_internal_debug_msgs/msg/detail/processing_time_tree__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace autoware_internal_debug_msgs
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void ProcessingTimeTree_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) autoware_internal_debug_msgs::msg::ProcessingTimeTree(_init);
}

void ProcessingTimeTree_fini_function(void * message_memory)
{
  auto typed_message = static_cast<autoware_internal_debug_msgs::msg::ProcessingTimeTree *>(message_memory);
  typed_message->~ProcessingTimeTree();
}

size_t size_function__ProcessingTimeTree__nodes(const void * untyped_member)
{
  const auto * member = reinterpret_cast<const std::vector<autoware_internal_debug_msgs::msg::ProcessingTimeNode> *>(untyped_member);
  return member->size();
}

const void * get_const_function__ProcessingTimeTree__nodes(const void * untyped_member, size_t index)
{
  const auto & member =
    *reinterpret_cast<const std::vector<autoware_internal_debug_msgs::msg::ProcessingTimeNode> *>(untyped_member);
  return &member[index];
}

void * get_function__ProcessingTimeTree__nodes(void * untyped_member, size_t index)
{
  auto & member =
    *reinterpret_cast<std::vector<autoware_internal_debug_msgs::msg::ProcessingTimeNode> *>(untyped_member);
  return &member[index];
}

void fetch_function__ProcessingTimeTree__nodes(
  const void * untyped_member, size_t index, void * untyped_value)
{
  const auto & item = *reinterpret_cast<const autoware_internal_debug_msgs::msg::ProcessingTimeNode *>(
    get_const_function__ProcessingTimeTree__nodes(untyped_member, index));
  auto & value = *reinterpret_cast<autoware_internal_debug_msgs::msg::ProcessingTimeNode *>(untyped_value);
  value = item;
}

void assign_function__ProcessingTimeTree__nodes(
  void * untyped_member, size_t index, const void * untyped_value)
{
  auto & item = *reinterpret_cast<autoware_internal_debug_msgs::msg::ProcessingTimeNode *>(
    get_function__ProcessingTimeTree__nodes(untyped_member, index));
  const auto & value = *reinterpret_cast<const autoware_internal_debug_msgs::msg::ProcessingTimeNode *>(untyped_value);
  item = value;
}

void resize_function__ProcessingTimeTree__nodes(void * untyped_member, size_t size)
{
  auto * member =
    reinterpret_cast<std::vector<autoware_internal_debug_msgs::msg::ProcessingTimeNode> *>(untyped_member);
  member->resize(size);
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember ProcessingTimeTree_message_member_array[1] = {
  {
    "nodes",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    ::rosidl_typesupport_introspection_cpp::get_message_type_support_handle<autoware_internal_debug_msgs::msg::ProcessingTimeNode>(),  // members of sub message
    true,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(autoware_internal_debug_msgs::msg::ProcessingTimeTree, nodes),  // bytes offset in struct
    nullptr,  // default value
    size_function__ProcessingTimeTree__nodes,  // size() function pointer
    get_const_function__ProcessingTimeTree__nodes,  // get_const(index) function pointer
    get_function__ProcessingTimeTree__nodes,  // get(index) function pointer
    fetch_function__ProcessingTimeTree__nodes,  // fetch(index, &value) function pointer
    assign_function__ProcessingTimeTree__nodes,  // assign(index, value) function pointer
    resize_function__ProcessingTimeTree__nodes  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers ProcessingTimeTree_message_members = {
  "autoware_internal_debug_msgs::msg",  // message namespace
  "ProcessingTimeTree",  // message name
  1,  // number of fields
  sizeof(autoware_internal_debug_msgs::msg::ProcessingTimeTree),
  ProcessingTimeTree_message_member_array,  // message members
  ProcessingTimeTree_init_function,  // function to initialize message memory (memory has to be allocated)
  ProcessingTimeTree_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t ProcessingTimeTree_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &ProcessingTimeTree_message_members,
  get_message_typesupport_handle_function,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace autoware_internal_debug_msgs


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<autoware_internal_debug_msgs::msg::ProcessingTimeTree>()
{
  return &::autoware_internal_debug_msgs::msg::rosidl_typesupport_introspection_cpp::ProcessingTimeTree_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, autoware_internal_debug_msgs, msg, ProcessingTimeTree)() {
  return &::autoware_internal_debug_msgs::msg::rosidl_typesupport_introspection_cpp::ProcessingTimeTree_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
