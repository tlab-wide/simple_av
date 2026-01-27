// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/CollisionPredictionInfo.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/collision_prediction_info__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'object_position'
#include "geometry_msgs/msg/detail/point__traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const CollisionPredictionInfo & msg,
  std::ostream & out)
{
  out << "{";
  // member: object_position
  {
    out << "object_position: ";
    to_flow_style_yaml(msg.object_position, out);
    out << ", ";
  }

  // member: time_to_collision
  {
    out << "time_to_collision: ";
    rosidl_generator_traits::value_to_yaml(msg.time_to_collision, out);
    out << ", ";
  }

  // member: object_label
  {
    out << "object_label: ";
    rosidl_generator_traits::value_to_yaml(msg.object_label, out);
    out << ", ";
  }

  // member: object_velocity
  {
    out << "object_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.object_velocity, out);
    out << ", ";
  }

  // member: collision_detected
  {
    out << "collision_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.collision_detected, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CollisionPredictionInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: object_position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_position:\n";
    to_block_style_yaml(msg.object_position, out, indentation + 2);
  }

  // member: time_to_collision
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "time_to_collision: ";
    rosidl_generator_traits::value_to_yaml(msg.time_to_collision, out);
    out << "\n";
  }

  // member: object_label
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_label: ";
    rosidl_generator_traits::value_to_yaml(msg.object_label, out);
    out << "\n";
  }

  // member: object_velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "object_velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.object_velocity, out);
    out << "\n";
  }

  // member: collision_detected
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "collision_detected: ";
    rosidl_generator_traits::value_to_yaml(msg.collision_detected, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CollisionPredictionInfo & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::CollisionPredictionInfo & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::CollisionPredictionInfo & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::CollisionPredictionInfo>()
{
  return "simple_av_msgs::msg::CollisionPredictionInfo";
}

template<>
inline const char * name<simple_av_msgs::msg::CollisionPredictionInfo>()
{
  return "simple_av_msgs/msg/CollisionPredictionInfo";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::CollisionPredictionInfo>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::CollisionPredictionInfo>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value> {};

template<>
struct is_message<simple_av_msgs::msg::CollisionPredictionInfo>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__TRAITS_HPP_
