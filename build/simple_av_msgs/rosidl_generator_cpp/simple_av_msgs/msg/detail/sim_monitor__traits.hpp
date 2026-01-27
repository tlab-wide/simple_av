// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/SimMonitor.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/sim_monitor__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const SimMonitor & msg,
  std::ostream & out)
{
  out << "{";
  // member: system_time
  {
    out << "system_time: ";
    rosidl_generator_traits::value_to_yaml(msg.system_time, out);
    out << ", ";
  }

  // member: sim_time
  {
    out << "sim_time: ";
    rosidl_generator_traits::value_to_yaml(msg.sim_time, out);
    out << ", ";
  }

  // member: sim_clock_rate
  {
    out << "sim_clock_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.sim_clock_rate, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SimMonitor & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: system_time
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "system_time: ";
    rosidl_generator_traits::value_to_yaml(msg.system_time, out);
    out << "\n";
  }

  // member: sim_time
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sim_time: ";
    rosidl_generator_traits::value_to_yaml(msg.sim_time, out);
    out << "\n";
  }

  // member: sim_clock_rate
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "sim_clock_rate: ";
    rosidl_generator_traits::value_to_yaml(msg.sim_clock_rate, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SimMonitor & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::SimMonitor & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::SimMonitor & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::SimMonitor>()
{
  return "simple_av_msgs::msg::SimMonitor";
}

template<>
inline const char * name<simple_av_msgs::msg::SimMonitor>()
{
  return "simple_av_msgs/msg/SimMonitor";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::SimMonitor>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::SimMonitor>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<simple_av_msgs::msg::SimMonitor>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__TRAITS_HPP_
