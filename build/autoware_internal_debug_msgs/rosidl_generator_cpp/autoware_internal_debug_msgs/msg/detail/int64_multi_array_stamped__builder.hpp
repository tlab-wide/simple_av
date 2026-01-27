// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_internal_debug_msgs:msg/Int64MultiArrayStamped.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__INT64_MULTI_ARRAY_STAMPED__BUILDER_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__INT64_MULTI_ARRAY_STAMPED__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_internal_debug_msgs/msg/detail/int64_multi_array_stamped__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_internal_debug_msgs
{

namespace msg
{

namespace builder
{

class Init_Int64MultiArrayStamped_data
{
public:
  explicit Init_Int64MultiArrayStamped_data(::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped & msg)
  : msg_(msg)
  {}
  ::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped data(::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped msg_;
};

class Init_Int64MultiArrayStamped_layout
{
public:
  explicit Init_Int64MultiArrayStamped_layout(::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped & msg)
  : msg_(msg)
  {}
  Init_Int64MultiArrayStamped_data layout(::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped::_layout_type arg)
  {
    msg_.layout = std::move(arg);
    return Init_Int64MultiArrayStamped_data(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped msg_;
};

class Init_Int64MultiArrayStamped_stamp
{
public:
  Init_Int64MultiArrayStamped_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Int64MultiArrayStamped_layout stamp(::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_Int64MultiArrayStamped_layout(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_internal_debug_msgs::msg::Int64MultiArrayStamped>()
{
  return autoware_internal_debug_msgs::msg::builder::Init_Int64MultiArrayStamped_stamp();
}

}  // namespace autoware_internal_debug_msgs

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__INT64_MULTI_ARRAY_STAMPED__BUILDER_HPP_
