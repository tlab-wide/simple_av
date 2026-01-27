// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/PlanningInternalMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/planning_internal_msg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const PlanningInternalMsg & msg,
  std::ostream & out)
{
  out << "{";
  // member: is_curve_detected
  {
    out << "is_curve_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.is_curve_detected, out);
    out << ", ";
  }

  // member: is_end_of_path
  {
    out << "is_end_of_path: ";
    rosidl_generator_traits::value_to_yaml(msg.is_end_of_path, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PlanningInternalMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: is_curve_detected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_curve_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.is_curve_detected, out);
    out << "\n";
  }

  // member: is_end_of_path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_end_of_path: ";
    rosidl_generator_traits::value_to_yaml(msg.is_end_of_path, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PlanningInternalMsg & msg, bool use_flow_style = false)
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

}  // namespace simple_av_msgs

namespace rosidl_generator_traits
{

[[deprecated("use simple_av_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const simple_av_msgs::msg::PlanningInternalMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::PlanningInternalMsg & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::PlanningInternalMsg>()
{
  return "simple_av_msgs::msg::PlanningInternalMsg";
}

template<>
inline const char * name<simple_av_msgs::msg::PlanningInternalMsg>()
{
  return "simple_av_msgs/msg/PlanningInternalMsg";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::PlanningInternalMsg>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::PlanningInternalMsg>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<simple_av_msgs::msg::PlanningInternalMsg>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__TRAITS_HPP_
