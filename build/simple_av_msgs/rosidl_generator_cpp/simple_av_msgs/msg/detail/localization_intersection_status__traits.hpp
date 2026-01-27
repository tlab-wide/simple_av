// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/LocalizationIntersectionStatus.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/localization_intersection_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const LocalizationIntersectionStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: intersection_name
  {
    out << "intersection_name: ";
    rosidl_generator_traits::value_to_yaml(msg.intersection_name, out);
    out << ", ";
  }

  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: distance_to_intersection
  {
    out << "distance_to_intersection: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_to_intersection, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const LocalizationIntersectionStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: intersection_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "intersection_name: ";
    rosidl_generator_traits::value_to_yaml(msg.intersection_name, out);
    out << "\n";
  }

  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: distance_to_intersection
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance_to_intersection: ";
    rosidl_generator_traits::value_to_yaml(msg.distance_to_intersection, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LocalizationIntersectionStatus & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::LocalizationIntersectionStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::LocalizationIntersectionStatus & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::LocalizationIntersectionStatus>()
{
  return "simple_av_msgs::msg::LocalizationIntersectionStatus";
}

template<>
inline const char * name<simple_av_msgs::msg::LocalizationIntersectionStatus>()
{
  return "simple_av_msgs/msg/LocalizationIntersectionStatus";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::LocalizationIntersectionStatus>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::LocalizationIntersectionStatus>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<simple_av_msgs::msg::LocalizationIntersectionStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__TRAITS_HPP_
