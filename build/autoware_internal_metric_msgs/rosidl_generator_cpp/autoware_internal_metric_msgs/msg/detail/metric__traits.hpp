// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from autoware_internal_metric_msgs:msg/Metric.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__TRAITS_HPP_
#define AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "autoware_internal_metric_msgs/msg/detail/metric__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace autoware_internal_metric_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Metric & msg,
  std::ostream & out)
{
  out << "{";
  // member: name
  {
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << ", ";
  }

  // member: unit
  {
    out << "unit: ";
    rosidl_generator_traits::value_to_yaml(msg.unit, out);
    out << ", ";
  }

  // member: value
  {
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Metric & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << "\n";
  }

  // member: unit
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "unit: ";
    rosidl_generator_traits::value_to_yaml(msg.unit, out);
    out << "\n";
  }

  // member: value
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "value: ";
    rosidl_generator_traits::value_to_yaml(msg.value, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Metric & msg, bool use_flow_style = false)
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
  const autoware_internal_metric_msgs::msg::Metric & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_internal_metric_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_internal_metric_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const autoware_internal_metric_msgs::msg::Metric & msg)
{
  return autoware_internal_metric_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_internal_metric_msgs::msg::Metric>()
{
  return "autoware_internal_metric_msgs::msg::Metric";
}

template<>
inline const char * name<autoware_internal_metric_msgs::msg::Metric>()
{
  return "autoware_internal_metric_msgs/msg/Metric";
}

template<>
struct has_fixed_size<autoware_internal_metric_msgs::msg::Metric>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<autoware_internal_metric_msgs::msg::Metric>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<autoware_internal_metric_msgs::msg::Metric>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__TRAITS_HPP_
