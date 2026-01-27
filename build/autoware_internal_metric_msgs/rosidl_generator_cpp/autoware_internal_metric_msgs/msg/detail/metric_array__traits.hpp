// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from autoware_internal_metric_msgs:msg/MetricArray.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__TRAITS_HPP_
#define AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "autoware_internal_metric_msgs/msg/detail/metric_array__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"
// Member 'metric_array'
#include "autoware_internal_metric_msgs/msg/detail/metric__traits.hpp"

namespace autoware_internal_metric_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const MetricArray & msg,
  std::ostream & out)
{
  out << "{";
  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
    out << ", ";
  }

  // member: metric_array
  {
    if (msg.metric_array.size() == 0) {
      out << "metric_array: []";
    } else {
      out << "metric_array: [";
      size_t pending_items = msg.metric_array.size();
      for (auto item : msg.metric_array) {
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
  const MetricArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }

  // member: metric_array
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.metric_array.size() == 0) {
      out << "metric_array: []\n";
    } else {
      out << "metric_array:\n";
      for (auto item : msg.metric_array) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const MetricArray & msg, bool use_flow_style = false)
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

}  // namespace autoware_internal_metric_msgs

namespace rosidl_generator_traits
{

[[deprecated("use autoware_internal_metric_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const autoware_internal_metric_msgs::msg::MetricArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_internal_metric_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_internal_metric_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const autoware_internal_metric_msgs::msg::MetricArray & msg)
{
  return autoware_internal_metric_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_internal_metric_msgs::msg::MetricArray>()
{
  return "autoware_internal_metric_msgs::msg::MetricArray";
}

template<>
inline const char * name<autoware_internal_metric_msgs::msg::MetricArray>()
{
  return "autoware_internal_metric_msgs/msg/MetricArray";
}

template<>
struct has_fixed_size<autoware_internal_metric_msgs::msg::MetricArray>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<autoware_internal_metric_msgs::msg::MetricArray>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<autoware_internal_metric_msgs::msg::MetricArray>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__TRAITS_HPP_
