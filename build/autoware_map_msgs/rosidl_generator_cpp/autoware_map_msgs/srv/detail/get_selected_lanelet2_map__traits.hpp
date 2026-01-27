// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from autoware_map_msgs:srv/GetSelectedLanelet2Map.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_MAP_MSGS__SRV__DETAIL__GET_SELECTED_LANELET2_MAP__TRAITS_HPP_
#define AUTOWARE_MAP_MSGS__SRV__DETAIL__GET_SELECTED_LANELET2_MAP__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "autoware_map_msgs/srv/detail/get_selected_lanelet2_map__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace autoware_map_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetSelectedLanelet2Map_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: cell_ids
  {
    if (msg.cell_ids.size() == 0) {
      out << "cell_ids: []";
    } else {
      out << "cell_ids: [";
      size_t pending_items = msg.cell_ids.size();
      for (auto item : msg.cell_ids) {
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
  const GetSelectedLanelet2Map_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: cell_ids
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.cell_ids.size() == 0) {
      out << "cell_ids: []\n";
    } else {
      out << "cell_ids:\n";
      for (auto item : msg.cell_ids) {
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

inline std::string to_yaml(const GetSelectedLanelet2Map_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace autoware_map_msgs

namespace rosidl_generator_traits
{

[[deprecated("use autoware_map_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const autoware_map_msgs::srv::GetSelectedLanelet2Map_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_map_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_map_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const autoware_map_msgs::srv::GetSelectedLanelet2Map_Request & msg)
{
  return autoware_map_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request>()
{
  return "autoware_map_msgs::srv::GetSelectedLanelet2Map_Request";
}

template<>
inline const char * name<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request>()
{
  return "autoware_map_msgs/srv/GetSelectedLanelet2Map_Request";
}

template<>
struct has_fixed_size<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"
// Member 'lanelet2_cells'
#include "autoware_map_msgs/msg/detail/lanelet_map_bin__traits.hpp"

namespace autoware_map_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const GetSelectedLanelet2Map_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: lanelet2_cells
  {
    out << "lanelet2_cells: ";
    to_flow_style_yaml(msg.lanelet2_cells, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const GetSelectedLanelet2Map_Response & msg,
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

  // member: lanelet2_cells
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "lanelet2_cells:\n";
    to_block_style_yaml(msg.lanelet2_cells, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const GetSelectedLanelet2Map_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace autoware_map_msgs

namespace rosidl_generator_traits
{

[[deprecated("use autoware_map_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const autoware_map_msgs::srv::GetSelectedLanelet2Map_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_map_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_map_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const autoware_map_msgs::srv::GetSelectedLanelet2Map_Response & msg)
{
  return autoware_map_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response>()
{
  return "autoware_map_msgs::srv::GetSelectedLanelet2Map_Response";
}

template<>
inline const char * name<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response>()
{
  return "autoware_map_msgs/srv/GetSelectedLanelet2Map_Response";
}

template<>
struct has_fixed_size<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response>
  : std::integral_constant<bool, has_fixed_size<autoware_map_msgs::msg::LaneletMapBin>::value && has_fixed_size<std_msgs::msg::Header>::value> {};

template<>
struct has_bounded_size<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response>
  : std::integral_constant<bool, has_bounded_size<autoware_map_msgs::msg::LaneletMapBin>::value && has_bounded_size<std_msgs::msg::Header>::value> {};

template<>
struct is_message<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<autoware_map_msgs::srv::GetSelectedLanelet2Map>()
{
  return "autoware_map_msgs::srv::GetSelectedLanelet2Map";
}

template<>
inline const char * name<autoware_map_msgs::srv::GetSelectedLanelet2Map>()
{
  return "autoware_map_msgs/srv/GetSelectedLanelet2Map";
}

template<>
struct has_fixed_size<autoware_map_msgs::srv::GetSelectedLanelet2Map>
  : std::integral_constant<
    bool,
    has_fixed_size<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request>::value &&
    has_fixed_size<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response>::value
  >
{
};

template<>
struct has_bounded_size<autoware_map_msgs::srv::GetSelectedLanelet2Map>
  : std::integral_constant<
    bool,
    has_bounded_size<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request>::value &&
    has_bounded_size<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response>::value
  >
{
};

template<>
struct is_service<autoware_map_msgs::srv::GetSelectedLanelet2Map>
  : std::true_type
{
};

template<>
struct is_service_request<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request>
  : std::true_type
{
};

template<>
struct is_service_response<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AUTOWARE_MAP_MSGS__SRV__DETAIL__GET_SELECTED_LANELET2_MAP__TRAITS_HPP_
