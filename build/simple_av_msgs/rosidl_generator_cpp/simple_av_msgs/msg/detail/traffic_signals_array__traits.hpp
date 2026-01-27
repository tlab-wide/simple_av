// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/TrafficSignalsArray.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/traffic_signals_array__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const TrafficSignalsArray & msg,
  std::ostream & out)
{
  out << "{";
  // member: v2i_traffic_signals_id
  {
    if (msg.v2i_traffic_signals_id.size() == 0) {
      out << "v2i_traffic_signals_id: []";
    } else {
      out << "v2i_traffic_signals_id: [";
      size_t pending_items = msg.v2i_traffic_signals_id.size();
      for (auto item : msg.v2i_traffic_signals_id) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: v2i_traffic_signals_colors
  {
    if (msg.v2i_traffic_signals_colors.size() == 0) {
      out << "v2i_traffic_signals_colors: []";
    } else {
      out << "v2i_traffic_signals_colors: [";
      size_t pending_items = msg.v2i_traffic_signals_colors.size();
      for (auto item : msg.v2i_traffic_signals_colors) {
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
  const TrafficSignalsArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: v2i_traffic_signals_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.v2i_traffic_signals_id.size() == 0) {
      out << "v2i_traffic_signals_id: []\n";
    } else {
      out << "v2i_traffic_signals_id:\n";
      for (auto item : msg.v2i_traffic_signals_id) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }

  // member: v2i_traffic_signals_colors
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.v2i_traffic_signals_colors.size() == 0) {
      out << "v2i_traffic_signals_colors: []\n";
    } else {
      out << "v2i_traffic_signals_colors:\n";
      for (auto item : msg.v2i_traffic_signals_colors) {
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

inline std::string to_yaml(const TrafficSignalsArray & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::TrafficSignalsArray & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::TrafficSignalsArray & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::TrafficSignalsArray>()
{
  return "simple_av_msgs::msg::TrafficSignalsArray";
}

template<>
inline const char * name<simple_av_msgs::msg::TrafficSignalsArray>()
{
  return "simple_av_msgs/msg/TrafficSignalsArray";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::TrafficSignalsArray>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::TrafficSignalsArray>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<simple_av_msgs::msg::TrafficSignalsArray>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__TRAITS_HPP_
