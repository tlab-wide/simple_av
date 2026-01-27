// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from autoware_perception_msgs:msg/PredictedTrafficLightState.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__TRAITS_HPP_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "autoware_perception_msgs/msg/detail/predicted_traffic_light_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'predicted_stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"
// Member 'simultaneous_elements'
#include "autoware_perception_msgs/msg/detail/traffic_light_element__traits.hpp"

namespace autoware_perception_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const PredictedTrafficLightState & msg,
  std::ostream & out)
{
  out << "{";
  // member: predicted_stamp
  {
    out << "predicted_stamp: ";
    to_flow_style_yaml(msg.predicted_stamp, out);
    out << ", ";
  }

  // member: simultaneous_elements
  {
    if (msg.simultaneous_elements.size() == 0) {
      out << "simultaneous_elements: []";
    } else {
      out << "simultaneous_elements: [";
      size_t pending_items = msg.simultaneous_elements.size();
      for (auto item : msg.simultaneous_elements) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: reliability
  {
    out << "reliability: ";
    rosidl_generator_traits::value_to_yaml(msg.reliability, out);
    out << ", ";
  }

  // member: information_source
  {
    out << "information_source: ";
    rosidl_generator_traits::value_to_yaml(msg.information_source, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PredictedTrafficLightState & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: predicted_stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "predicted_stamp:\n";
    to_block_style_yaml(msg.predicted_stamp, out, indentation + 2);
  }

  // member: simultaneous_elements
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.simultaneous_elements.size() == 0) {
      out << "simultaneous_elements: []\n";
    } else {
      out << "simultaneous_elements:\n";
      for (auto item : msg.simultaneous_elements) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: reliability
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "reliability: ";
    rosidl_generator_traits::value_to_yaml(msg.reliability, out);
    out << "\n";
  }

  // member: information_source
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "information_source: ";
    rosidl_generator_traits::value_to_yaml(msg.information_source, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PredictedTrafficLightState & msg, bool use_flow_style = false)
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

}  // namespace autoware_perception_msgs

namespace rosidl_generator_traits
{

[[deprecated("use autoware_perception_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const autoware_perception_msgs::msg::PredictedTrafficLightState & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_perception_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_perception_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const autoware_perception_msgs::msg::PredictedTrafficLightState & msg)
{
  return autoware_perception_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_perception_msgs::msg::PredictedTrafficLightState>()
{
  return "autoware_perception_msgs::msg::PredictedTrafficLightState";
}

template<>
inline const char * name<autoware_perception_msgs::msg::PredictedTrafficLightState>()
{
  return "autoware_perception_msgs/msg/PredictedTrafficLightState";
}

template<>
struct has_fixed_size<autoware_perception_msgs::msg::PredictedTrafficLightState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<autoware_perception_msgs::msg::PredictedTrafficLightState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<autoware_perception_msgs::msg::PredictedTrafficLightState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__TRAITS_HPP_
