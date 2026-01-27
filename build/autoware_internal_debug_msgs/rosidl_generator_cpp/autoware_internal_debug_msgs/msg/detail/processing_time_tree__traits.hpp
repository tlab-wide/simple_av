// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeTree.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__TRAITS_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "autoware_internal_debug_msgs/msg/detail/processing_time_tree__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'nodes'
#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__traits.hpp"

namespace autoware_internal_debug_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const ProcessingTimeTree & msg,
  std::ostream & out)
{
  out << "{";
  // member: nodes
  {
    if (msg.nodes.size() == 0) {
      out << "nodes: []";
    } else {
      out << "nodes: [";
      size_t pending_items = msg.nodes.size();
      for (auto item : msg.nodes) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const ProcessingTimeTree & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: nodes
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.nodes.size() == 0) {
      out << "nodes: []\n";
    } else {
      out << "nodes:\n";
      for (auto item : msg.nodes) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const ProcessingTimeTree & msg, bool use_flow_style = false)
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
  const autoware_internal_debug_msgs::msg::ProcessingTimeTree & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_internal_debug_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_internal_debug_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const autoware_internal_debug_msgs::msg::ProcessingTimeTree & msg)
{
  return autoware_internal_debug_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_internal_debug_msgs::msg::ProcessingTimeTree>()
{
  return "autoware_internal_debug_msgs::msg::ProcessingTimeTree";
}

template<>
inline const char * name<autoware_internal_debug_msgs::msg::ProcessingTimeTree>()
{
  return "autoware_internal_debug_msgs/msg/ProcessingTimeTree";
}

template<>
struct has_fixed_size<autoware_internal_debug_msgs::msg::ProcessingTimeTree>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<autoware_internal_debug_msgs::msg::ProcessingTimeTree>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<autoware_internal_debug_msgs::msg::ProcessingTimeTree>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__TRAITS_HPP_
