// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeTree.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__BUILDER_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_internal_debug_msgs/msg/detail/processing_time_tree__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_internal_debug_msgs
{

namespace msg
{

namespace builder
{

class Init_ProcessingTimeTree_nodes
{
public:
  Init_ProcessingTimeTree_nodes()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::autoware_internal_debug_msgs::msg::ProcessingTimeTree nodes(::autoware_internal_debug_msgs::msg::ProcessingTimeTree::_nodes_type arg)
  {
    msg_.nodes = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ProcessingTimeTree msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_internal_debug_msgs::msg::ProcessingTimeTree>()
{
  return autoware_internal_debug_msgs::msg::builder::Init_ProcessingTimeTree_nodes();
}

}  // namespace autoware_internal_debug_msgs

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__BUILDER_HPP_
