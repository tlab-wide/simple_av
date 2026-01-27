// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_internal_debug_msgs:srv/String.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__BUILDER_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_internal_debug_msgs/srv/detail/string__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_internal_debug_msgs
{

namespace srv
{

namespace builder
{

class Init_String_Request_data
{
public:
  Init_String_Request_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::autoware_internal_debug_msgs::srv::String_Request data(::autoware_internal_debug_msgs::srv::String_Request::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_internal_debug_msgs::srv::String_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_internal_debug_msgs::srv::String_Request>()
{
  return autoware_internal_debug_msgs::srv::builder::Init_String_Request_data();
}

}  // namespace autoware_internal_debug_msgs


namespace autoware_internal_debug_msgs
{

namespace srv
{

namespace builder
{

class Init_String_Response_success
{
public:
  Init_String_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::autoware_internal_debug_msgs::srv::String_Response success(::autoware_internal_debug_msgs::srv::String_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_internal_debug_msgs::srv::String_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_internal_debug_msgs::srv::String_Response>()
{
  return autoware_internal_debug_msgs::srv::builder::Init_String_Response_success();
}

}  // namespace autoware_internal_debug_msgs

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__BUILDER_HPP_
