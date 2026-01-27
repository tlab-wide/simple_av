// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:msg/DetectedObject.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__TRAITS_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/msg/detail/detected_object__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'position'
// Member 'bounding_box'
#include "geometry_msgs/msg/detail/point__traits.hpp"
// Member 'orientation'
#include "geometry_msgs/msg/detail/quaternion__traits.hpp"
// Member 'shape'
#include "geometry_msgs/msg/detail/vector3__traits.hpp"
// Member 'relative_direction'
#include "std_msgs/msg/detail/string__traits.hpp"

namespace simple_av_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const DetectedObject & msg,
  std::ostream & out)
{
  out << "{";
  // member: is_from_rsu
  {
    out << "is_from_rsu: ";
    rosidl_generator_traits::value_to_yaml(msg.is_from_rsu, out);
    out << ", ";
  }

  // member: label
  {
    out << "label: ";
    rosidl_generator_traits::value_to_yaml(msg.label, out);
    out << ", ";
  }

  // member: position
  {
    out << "position: ";
    to_flow_style_yaml(msg.position, out);
    out << ", ";
  }

  // member: velocity
  {
    out << "velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.velocity, out);
    out << ", ";
  }

  // member: orientation
  {
    out << "orientation: ";
    to_flow_style_yaml(msg.orientation, out);
    out << ", ";
  }

  // member: shape
  {
    out << "shape: ";
    to_flow_style_yaml(msg.shape, out);
    out << ", ";
  }

  // member: relative_direction
  {
    out << "relative_direction: ";
    to_flow_style_yaml(msg.relative_direction, out);
    out << ", ";
  }

  // member: bounding_box
  {
    if (msg.bounding_box.size() == 0) {
      out << "bounding_box: []";
    } else {
      out << "bounding_box: [";
      size_t pending_items = msg.bounding_box.size();
      for (auto item : msg.bounding_box) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: distance
  {
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
    out << ", ";
  }

  // member: nearest_object_side
  {
    out << "nearest_object_side: ";
    rosidl_generator_traits::value_to_yaml(msg.nearest_object_side, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const DetectedObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: is_from_rsu
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_from_rsu: ";
    rosidl_generator_traits::value_to_yaml(msg.is_from_rsu, out);
    out << "\n";
  }

  // member: label
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "label: ";
    rosidl_generator_traits::value_to_yaml(msg.label, out);
    out << "\n";
  }

  // member: position
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "position:\n";
    to_block_style_yaml(msg.position, out, indentation + 2);
  }

  // member: velocity
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "velocity: ";
    rosidl_generator_traits::value_to_yaml(msg.velocity, out);
    out << "\n";
  }

  // member: orientation
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "orientation:\n";
    to_block_style_yaml(msg.orientation, out, indentation + 2);
  }

  // member: shape
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "shape:\n";
    to_block_style_yaml(msg.shape, out, indentation + 2);
  }

  // member: relative_direction
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "relative_direction:\n";
    to_block_style_yaml(msg.relative_direction, out, indentation + 2);
  }

  // member: bounding_box
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.bounding_box.size() == 0) {
      out << "bounding_box: []\n";
    } else {
      out << "bounding_box:\n";
      for (auto item : msg.bounding_box) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: distance
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distance: ";
    rosidl_generator_traits::value_to_yaml(msg.distance, out);
    out << "\n";
  }

  // member: nearest_object_side
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "nearest_object_side: ";
    rosidl_generator_traits::value_to_yaml(msg.nearest_object_side, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const DetectedObject & msg, bool use_flow_style = false)
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
  const simple_av_msgs::msg::DetectedObject & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::msg::DetectedObject & msg)
{
  return simple_av_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::msg::DetectedObject>()
{
  return "simple_av_msgs::msg::DetectedObject";
}

template<>
inline const char * name<simple_av_msgs::msg::DetectedObject>()
{
  return "simple_av_msgs/msg/DetectedObject";
}

template<>
struct has_fixed_size<simple_av_msgs::msg::DetectedObject>
  : std::integral_constant<bool, has_fixed_size<geometry_msgs::msg::Point>::value && has_fixed_size<geometry_msgs::msg::Quaternion>::value && has_fixed_size<geometry_msgs::msg::Vector3>::value && has_fixed_size<std_msgs::msg::String>::value> {};

template<>
struct has_bounded_size<simple_av_msgs::msg::DetectedObject>
  : std::integral_constant<bool, has_bounded_size<geometry_msgs::msg::Point>::value && has_bounded_size<geometry_msgs::msg::Quaternion>::value && has_bounded_size<geometry_msgs::msg::Vector3>::value && has_bounded_size<std_msgs::msg::String>::value> {};

template<>
struct is_message<simple_av_msgs::msg::DetectedObject>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__TRAITS_HPP_
