// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from autoware_map_msgs:msg/LaneletMapMetaData.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_META_DATA__TRAITS_HPP_
#define AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_META_DATA__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "autoware_map_msgs/msg/detail/lanelet_map_meta_data__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'metadata_list'
#include "autoware_map_msgs/msg/detail/lanelet_map_cell_meta_data__traits.hpp"

namespace autoware_map_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const LaneletMapMetaData & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: metadata_list
  {
    if (msg.metadata_list.size() == 0) {
      out << "metadata_list: []";
    } else {
      out << "metadata_list: [";
      size_t pending_items = msg.metadata_list.size();
      for (auto item : msg.metadata_list) {
        to_flow_style_yaml(item, out);
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
  const LaneletMapMetaData & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: metadata_list
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.metadata_list.size() == 0) {
      out << "metadata_list: []\n";
    } else {
      out << "metadata_list:\n";
      for (auto item : msg.metadata_list) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const LaneletMapMetaData & msg, bool use_flow_style = false)
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

}  // namespace autoware_map_msgs

namespace rosidl_generator_traits
{

[[deprecated("use autoware_map_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const autoware_map_msgs::msg::LaneletMapMetaData & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_map_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_map_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const autoware_map_msgs::msg::LaneletMapMetaData & msg)
{
  return autoware_map_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_map_msgs::msg::LaneletMapMetaData>()
{
  return "autoware_map_msgs::msg::LaneletMapMetaData";
}

template<>
inline const char * name<autoware_map_msgs::msg::LaneletMapMetaData>()
{
  return "autoware_map_msgs/msg/LaneletMapMetaData";
}

template<>
struct has_fixed_size<autoware_map_msgs::msg::LaneletMapMetaData>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<autoware_map_msgs::msg::LaneletMapMetaData>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<autoware_map_msgs::msg::LaneletMapMetaData>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_META_DATA__TRAITS_HPP_
