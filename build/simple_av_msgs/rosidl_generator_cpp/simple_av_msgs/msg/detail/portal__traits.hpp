// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/Portal.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/portal__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const Portal & msg,
  std::ostream & out)
{
  out << "{";
  // member: reset
  {
    out << "reset: ";
    rosidl_generator_traits::value_to_yaml(msg.reset, out);
    out << ", ";
  }

  // member: round_number
  {
    out << "round_number: ";
    rosidl_generator_traits::value_to_yaml(msg.round_number, out);
    out << ", ";
  }

  // member: finished
  {
    out << "finished: ";
    rosidl_generator_traits::value_to_yaml(msg.finished, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Portal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: reset
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reset: ";
    rosidl_generator_traits::value_to_yaml(msg.reset, out);
    out << "\n";
  }

  // member: round_number
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "round_number: ";
    rosidl_generator_traits::value_to_yaml(msg.round_number, out);
    out << "\n";
  }

  // member: finished
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "finished: ";
    rosidl_generator_traits::value_to_yaml(msg.finished, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Portal & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::Portal & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::Portal & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::Portal>()
{
  return "simple_av_msgs::msg::Portal";
}

template<>
inline const char * name<simple_av_msgs::msg::Portal>()
{
  return "simple_av_msgs/msg/Portal";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::Portal>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::Portal>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<simple_av_msgs::msg::Portal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__TRAITS_HPP_
