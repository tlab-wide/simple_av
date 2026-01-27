// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from simple_av_msgs:srv/TriggerMissionPlan.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__TRAITS_HPP_
#define SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "simple_av_msgs/srv/detail/trigger_mission_plan__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace simple_av_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const TriggerMissionPlan_Request & msg,
  std::ostream & out)
{
  (void)msg;
  out << "null";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TriggerMissionPlan_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  (void)msg;
  (void)indentation;
  out << "null\n";
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TriggerMissionPlan_Request & msg, bool use_flow_style = false)
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

}  // namespace simple_av_msgs

namespace rosidl_generator_traits
{

[[deprecated("use simple_av_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const simple_av_msgs::srv::TriggerMissionPlan_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::srv::TriggerMissionPlan_Request & msg)
{
  return simple_av_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::srv::TriggerMissionPlan_Request>()
{
  return "simple_av_msgs::srv::TriggerMissionPlan_Request";
}

template<>
inline const char * name<simple_av_msgs::srv::TriggerMissionPlan_Request>()
{
  return "simple_av_msgs/srv/TriggerMissionPlan_Request";
}

template<>
struct has_fixed_size<simple_av_msgs::srv::TriggerMissionPlan_Request>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<simple_av_msgs::srv::TriggerMissionPlan_Request>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<simple_av_msgs::srv::TriggerMissionPlan_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace simple_av_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const TriggerMissionPlan_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const TriggerMissionPlan_Response & msg,
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

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const TriggerMissionPlan_Response & msg, bool use_flow_style = false)
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

}  // namespace simple_av_msgs

namespace rosidl_generator_traits
{

[[deprecated("use simple_av_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const simple_av_msgs::srv::TriggerMissionPlan_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  simple_av_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use simple_av_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const simple_av_msgs::srv::TriggerMissionPlan_Response & msg)
{
  return simple_av_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<simple_av_msgs::srv::TriggerMissionPlan_Response>()
{
  return "simple_av_msgs::srv::TriggerMissionPlan_Response";
}

template<>
inline const char * name<simple_av_msgs::srv::TriggerMissionPlan_Response>()
{
  return "simple_av_msgs/srv/TriggerMissionPlan_Response";
}

template<>
struct has_fixed_size<simple_av_msgs::srv::TriggerMissionPlan_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<simple_av_msgs::srv::TriggerMissionPlan_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<simple_av_msgs::srv::TriggerMissionPlan_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<simple_av_msgs::srv::TriggerMissionPlan>()
{
  return "simple_av_msgs::srv::TriggerMissionPlan";
}

template<>
inline const char * name<simple_av_msgs::srv::TriggerMissionPlan>()
{
  return "simple_av_msgs/srv/TriggerMissionPlan";
}

template<>
struct has_fixed_size<simple_av_msgs::srv::TriggerMissionPlan>
  : std::integral_constant<
    bool,
    has_fixed_size<simple_av_msgs::srv::TriggerMissionPlan_Request>::value &&
    has_fixed_size<simple_av_msgs::srv::TriggerMissionPlan_Response>::value
  >
{
};

template<>
struct has_bounded_size<simple_av_msgs::srv::TriggerMissionPlan>
  : std::integral_constant<
    bool,
    has_bounded_size<simple_av_msgs::srv::TriggerMissionPlan_Request>::value &&
    has_bounded_size<simple_av_msgs::srv::TriggerMissionPlan_Response>::value
  >
{
};

template<>
struct is_service<simple_av_msgs::srv::TriggerMissionPlan>
  : std::true_type
{
};

template<>
struct is_service_request<simple_av_msgs::srv::TriggerMissionPlan_Request>
  : std::true_type
{
};

template<>
struct is_service_response<simple_av_msgs::srv::TriggerMissionPlan_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__TRAITS_HPP_
