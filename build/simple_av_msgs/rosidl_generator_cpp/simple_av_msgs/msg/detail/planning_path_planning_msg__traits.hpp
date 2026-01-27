// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/PlanningPathPlanningMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/planning_path_planning_msg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'look_ahead_point'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const PlanningPathPlanningMsg & msg,
  std::ostream & out)
{
  out << "{";
  // member: look_ahead_point
  {
    out << "look_ahead_point: ";
    to_flow_style_yaml(msg.look_ahead_point, out);
    out << ", ";
  }

  // member: speed_limit
  {
    out << "speed_limit: ";
    rosidl_generator_traits::value_to_yaml(msg.speed_limit, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PlanningPathPlanningMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: look_ahead_point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "look_ahead_point:\n";
    to_block_style_yaml(msg.look_ahead_point, out, indentation + 2);
  }

  // member: speed_limit
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "speed_limit: ";
    rosidl_generator_traits::value_to_yaml(msg.speed_limit, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PlanningPathPlanningMsg & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::PlanningPathPlanningMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::PlanningPathPlanningMsg & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::PlanningPathPlanningMsg>()
{
  return "simple_av_msgs::msg::PlanningPathPlanningMsg";
}

template<>
inline const char * name<simple_av_msgs::msg::PlanningPathPlanningMsg>()
{
  return "simple_av_msgs/msg/PlanningPathPlanningMsg";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::PlanningPathPlanningMsg>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::PlanningPathPlanningMsg>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value> {};

template<>
struct is_message<simple_av_msgs::msg::PlanningPathPlanningMsg>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__TRAITS_HPP_
