// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeNode.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_NODE__TRAITS_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_NODE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace autoware_internal_debug_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ProcessingTimeNode & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: name
  {
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << ", ";
  }

  // member: processing_time
  {
    out << "processing_time: ";
    rosidl_generator_traits::value_to_yaml(msg.processing_time, out);
    out << ", ";
  }

  // member: parent_id
  {
    out << "parent_id: ";
    rosidl_generator_traits::value_to_yaml(msg.parent_id, out);
    out << ", ";
  }

  // member: comment
  {
    out << "comment: ";
    rosidl_generator_traits::value_to_yaml(msg.comment, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ProcessingTimeNode & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << "\n";
  }

  // member: processing_time
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "processing_time: ";
    rosidl_generator_traits::value_to_yaml(msg.processing_time, out);
    out << "\n";
  }

  // member: parent_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "parent_id: ";
    rosidl_generator_traits::value_to_yaml(msg.parent_id, out);
    out << "\n";
  }

  // member: comment
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "comment: ";
    rosidl_generator_traits::value_to_yaml(msg.comment, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ProcessingTimeNode & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace autoware_internal_debug_msgs

namespace rosidl_generator_traits
{

[[deprecated("use autoware_internal_debug_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const autoware_internal_debug_msgs::msg::ProcessingTimeNode & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_internal_debug_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_internal_debug_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const autoware_internal_debug_msgs::msg::ProcessingTimeNode & msg)
{
  return autoware_internal_debug_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_internal_debug_msgs::msg::ProcessingTimeNode>()
{
  return "autoware_internal_debug_msgs::msg::ProcessingTimeNode";
}

template<>
inline const char * name<autoware_internal_debug_msgs::msg::ProcessingTimeNode>()
{
  return "autoware_internal_debug_msgs/msg/ProcessingTimeNode";
}

template<>
struct has_fixed_size<autoware_internal_debug_msgs::msg::ProcessingTimeNode>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<autoware_internal_debug_msgs::msg::ProcessingTimeNode>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<autoware_internal_debug_msgs::msg::ProcessingTimeNode>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_NODE__TRAITS_HPP_
