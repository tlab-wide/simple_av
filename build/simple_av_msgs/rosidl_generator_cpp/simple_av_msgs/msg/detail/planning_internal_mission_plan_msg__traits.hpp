// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/PlanningInternalMissionPlanMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/planning_internal_mission_plan_msg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'path'
#include "simple_av_msgs/msg/detail/planning_waypoint__traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const PlanningInternalMissionPlanMsg & msg,
  std::ostream & out)
{
  out << "{";
  // member: path
  {
    if (msg.path.size() == 0) {
      out << "path: []";
    } else {
      out << "path: [";
      size_t pending_items = msg.path.size();
      for (auto item : msg.path) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: path_as_lanes
  {
    if (msg.path_as_lanes.size() == 0) {
      out << "path_as_lanes: []";
    } else {
      out << "path_as_lanes: [";
      size_t pending_items = msg.path_as_lanes.size();
      for (auto item : msg.path_as_lanes) {
        rosidl_generator_traits::value_to_yaml(item, out);
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
  const PlanningInternalMissionPlanMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: path
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.path.size() == 0) {
      out << "path: []\n";
    } else {
      out << "path:\n";
      for (auto item : msg.path) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: path_as_lanes
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.path_as_lanes.size() == 0) {
      out << "path_as_lanes: []\n";
    } else {
      out << "path_as_lanes:\n";
      for (auto item : msg.path_as_lanes) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PlanningInternalMissionPlanMsg & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::PlanningInternalMissionPlanMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::PlanningInternalMissionPlanMsg & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::PlanningInternalMissionPlanMsg>()
{
  return "simple_av_msgs::msg::PlanningInternalMissionPlanMsg";
}

template<>
inline const char * name<simple_av_msgs::msg::PlanningInternalMissionPlanMsg>()
{
  return "simple_av_msgs/msg/PlanningInternalMissionPlanMsg";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::PlanningInternalMissionPlanMsg>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::PlanningInternalMissionPlanMsg>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<simple_av_msgs::msg::PlanningInternalMissionPlanMsg>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__TRAITS_HPP_
