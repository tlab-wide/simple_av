// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/LocalizationMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/localization_msg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'closest_point'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'closest_lane_names'
#include "std_msgs/msg/detail/string__traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const LocalizationMsg & msg,
  std::ostream & out)
{
  out << "{";
  // member: closest_point
  {
    out << "closest_point: ";
    to_flow_style_yaml(msg.closest_point, out);
    out << ", ";
  }

  // member: closest_lane_names
  {
    out << "closest_lane_names: ";
    to_flow_style_yaml(msg.closest_lane_names, out);
    out << ", ";
  }

  // member: minimal_distance
  {
    out << "minimal_distance: ";
    rosidl_generator_traits::value_to_yaml(msg.minimal_distance, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LocalizationMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: closest_point
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "closest_point:\n";
    to_block_style_yaml(msg.closest_point, out, indentation + 2);
  }

  // member: closest_lane_names
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "closest_lane_names:\n";
    to_block_style_yaml(msg.closest_lane_names, out, indentation + 2);
  }

  // member: minimal_distance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "minimal_distance: ";
    rosidl_generator_traits::value_to_yaml(msg.minimal_distance, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LocalizationMsg & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::LocalizationMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::LocalizationMsg & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::LocalizationMsg>()
{
  return "simple_av_msgs::msg::LocalizationMsg";
}

template<>
inline const char * name<simple_av_msgs::msg::LocalizationMsg>()
{
  return "simple_av_msgs/msg/LocalizationMsg";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::LocalizationMsg>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value && has_fixed_size<std_msgs::msg::String>::value> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::LocalizationMsg>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value && has_bounded_size<std_msgs::msg::String>::value> {};

template<>
struct is_message<simple_av_msgs::msg::LocalizationMsg>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__TRAITS_HPP_
