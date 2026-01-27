// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from autoware_internal_debug_msgs:srv/String.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__TRAITS_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "autoware_internal_debug_msgs/srv/detail/string__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace autoware_internal_debug_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const String_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: data
  {
    out << "data: ";
    rosidl_generator_traits::value_to_yaml(msg.data, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const String_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: data
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "data: ";
    rosidl_generator_traits::value_to_yaml(msg.data, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const String_Request & msg, bool use_flow_style = false)
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

}  // namespace autoware_internal_debug_msgs

namespace rosidl_generator_traits
{

[[deprecated("use autoware_internal_debug_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const autoware_internal_debug_msgs::srv::String_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_internal_debug_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_internal_debug_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const autoware_internal_debug_msgs::srv::String_Request & msg)
{
  return autoware_internal_debug_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_internal_debug_msgs::srv::String_Request>()
{
  return "autoware_internal_debug_msgs::srv::String_Request";
}

template<>
inline const char * name<autoware_internal_debug_msgs::srv::String_Request>()
{
  return "autoware_internal_debug_msgs/srv/String_Request";
}

template<>
struct has_fixed_size<autoware_internal_debug_msgs::srv::String_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<autoware_internal_debug_msgs::srv::String_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<autoware_internal_debug_msgs::srv::String_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace autoware_internal_debug_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const String_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const String_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const String_Response & msg, bool use_flow_style = false)
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

}  // namespace autoware_internal_debug_msgs

namespace rosidl_generator_traits
{

[[deprecated("use autoware_internal_debug_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const autoware_internal_debug_msgs::srv::String_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  autoware_internal_debug_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use autoware_internal_debug_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const autoware_internal_debug_msgs::srv::String_Response & msg)
{
  return autoware_internal_debug_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<autoware_internal_debug_msgs::srv::String_Response>()
{
  return "autoware_internal_debug_msgs::srv::String_Response";
}

template<>
inline const char * name<autoware_internal_debug_msgs::srv::String_Response>()
{
  return "autoware_internal_debug_msgs/srv/String_Response";
}

template<>
struct has_fixed_size<autoware_internal_debug_msgs::srv::String_Response>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<autoware_internal_debug_msgs::srv::String_Response>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<autoware_internal_debug_msgs::srv::String_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<autoware_internal_debug_msgs::srv::String>()
{
  return "autoware_internal_debug_msgs::srv::String";
}

template<>
inline const char * name<autoware_internal_debug_msgs::srv::String>()
{
  return "autoware_internal_debug_msgs/srv/String";
}

template<>
struct has_fixed_size<autoware_internal_debug_msgs::srv::String>
  : std::integral_constant<
    bool,
    has_fixed_size<autoware_internal_debug_msgs::srv::String_Request>::value &&
    has_fixed_size<autoware_internal_debug_msgs::srv::String_Response>::value
  >
{
};

template<>
struct has_bounded_size<autoware_internal_debug_msgs::srv::String>
  : std::integral_constant<
    bool,
    has_bounded_size<autoware_internal_debug_msgs::srv::String_Request>::value &&
    has_bounded_size<autoware_internal_debug_msgs::srv::String_Response>::value
  >
{
};

template<>
struct is_service<autoware_internal_debug_msgs::srv::String>
  : std::true_type
{
};

template<>
struct is_service_request<autoware_internal_debug_msgs::srv::String_Request>
  : std::true_type
{
};

template<>
struct is_service_response<autoware_internal_debug_msgs::srv::String_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__TRAITS_HPP_
