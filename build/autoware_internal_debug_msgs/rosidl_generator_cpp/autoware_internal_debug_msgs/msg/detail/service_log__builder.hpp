// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_internal_debug_msgs:msg/ServiceLog.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__SERVICE_LOG__BUILDER_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__SERVICE_LOG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_internal_debug_msgs/msg/detail/service_log__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_internal_debug_msgs
{

namespace msg
{

namespace builder
{

class Init_ServiceLog_yaml
{
public:
  explicit Init_ServiceLog_yaml(::autoware_internal_debug_msgs::msg::ServiceLog & msg)
  : msg_(msg)
  {}
  ::autoware_internal_debug_msgs::msg::ServiceLog yaml(::autoware_internal_debug_msgs::msg::ServiceLog::_yaml_type arg)
  {
    msg_.yaml = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ServiceLog msg_;
};

class Init_ServiceLog_node
{
public:
  explicit Init_ServiceLog_node(::autoware_internal_debug_msgs::msg::ServiceLog & msg)
  : msg_(msg)
  {}
  Init_ServiceLog_yaml node(::autoware_internal_debug_msgs::msg::ServiceLog::_node_type arg)
  {
    msg_.node = std::move(arg);
    return Init_ServiceLog_yaml(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ServiceLog msg_;
};

class Init_ServiceLog_name
{
public:
  explicit Init_ServiceLog_name(::autoware_internal_debug_msgs::msg::ServiceLog & msg)
  : msg_(msg)
  {}
  Init_ServiceLog_node name(::autoware_internal_debug_msgs::msg::ServiceLog::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_ServiceLog_node(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ServiceLog msg_;
};

class Init_ServiceLog_type
{
public:
  explicit Init_ServiceLog_type(::autoware_internal_debug_msgs::msg::ServiceLog & msg)
  : msg_(msg)
  {}
  Init_ServiceLog_name type(::autoware_internal_debug_msgs::msg::ServiceLog::_type_type arg)
  {
    msg_.type = std::move(arg);
    return Init_ServiceLog_name(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ServiceLog msg_;
};

class Init_ServiceLog_stamp
{
public:
  Init_ServiceLog_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ServiceLog_type stamp(::autoware_internal_debug_msgs::msg::ServiceLog::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_ServiceLog_type(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ServiceLog msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_internal_debug_msgs::msg::ServiceLog>()
{
  return autoware_internal_debug_msgs::msg::builder::Init_ServiceLog_stamp();
}

}  // namespace autoware_internal_debug_msgs

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__SERVICE_LOG__BUILDER_HPP_
