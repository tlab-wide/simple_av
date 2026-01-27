// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/PlanningMotionPlanningMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/planning_motion_planning_msg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'stop_point'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'status'
// Member 'stop_reason'
#include "std_msgs/msg/detail/string__traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const PlanningMotionPlanningMsg & msg,
  std::ostream & out)
{
  out << "{";
  // member: stop_point
  {
    out << "stop_point: ";
    to_flow_style_yaml(msg.stop_point, out);
    out << ", ";
  }

  // member: status
  {
    out << "status: ";
    to_flow_style_yaml(msg.status, out);
    out << ", ";
  }

  // member: stop_reason
  {
    out << "stop_reason: ";
    to_flow_style_yaml(msg.stop_reason, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PlanningMotionPlanningMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: stop_point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stop_point:\n";
    to_block_style_yaml(msg.stop_point, out, indentation + 2);
  }

  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status:\n";
    to_block_style_yaml(msg.status, out, indentation + 2);
  }

  // member: stop_reason
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stop_reason:\n";
    to_block_style_yaml(msg.stop_reason, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PlanningMotionPlanningMsg & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::PlanningMotionPlanningMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::PlanningMotionPlanningMsg & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::PlanningMotionPlanningMsg>()
{
  return "simple_av_msgs::msg::PlanningMotionPlanningMsg";
}

template<>
inline const char * name<simple_av_msgs::msg::PlanningMotionPlanningMsg>()
{
  return "simple_av_msgs/msg/PlanningMotionPlanningMsg";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::PlanningMotionPlanningMsg>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value && has_fixed_size<std_msgs::msg::String>::value> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::PlanningMotionPlanningMsg>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value && has_bounded_size<std_msgs::msg::String>::value> {};

template<>
struct is_message<simple_av_msgs::msg::PlanningMotionPlanningMsg>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__TRAITS_HPP_
