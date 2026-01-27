// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeNode.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_NODE__BUILDER_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_NODE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_internal_debug_msgs
{

namespace msg
{

namespace builder
{

class Init_ProcessingTimeNode_comment
{
public:
  explicit Init_ProcessingTimeNode_comment(::autoware_internal_debug_msgs::msg::ProcessingTimeNode & msg)
  : msg_(msg)
  {}
  ::autoware_internal_debug_msgs::msg::ProcessingTimeNode comment(::autoware_internal_debug_msgs::msg::ProcessingTimeNode::_comment_type arg)
  {
    msg_.comment = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ProcessingTimeNode msg_;
};

class Init_ProcessingTimeNode_parent_id
{
public:
  explicit Init_ProcessingTimeNode_parent_id(::autoware_internal_debug_msgs::msg::ProcessingTimeNode & msg)
  : msg_(msg)
  {}
  Init_ProcessingTimeNode_comment parent_id(::autoware_internal_debug_msgs::msg::ProcessingTimeNode::_parent_id_type arg)
  {
    msg_.parent_id = std::move(arg);
    return Init_ProcessingTimeNode_comment(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ProcessingTimeNode msg_;
};

class Init_ProcessingTimeNode_processing_time
{
public:
  explicit Init_ProcessingTimeNode_processing_time(::autoware_internal_debug_msgs::msg::ProcessingTimeNode & msg)
  : msg_(msg)
  {}
  Init_ProcessingTimeNode_parent_id processing_time(::autoware_internal_debug_msgs::msg::ProcessingTimeNode::_processing_time_type arg)
  {
    msg_.processing_time = std::move(arg);
    return Init_ProcessingTimeNode_parent_id(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ProcessingTimeNode msg_;
};

class Init_ProcessingTimeNode_name
{
public:
  explicit Init_ProcessingTimeNode_name(::autoware_internal_debug_msgs::msg::ProcessingTimeNode & msg)
  : msg_(msg)
  {}
  Init_ProcessingTimeNode_processing_time name(::autoware_internal_debug_msgs::msg::ProcessingTimeNode::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_ProcessingTimeNode_processing_time(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ProcessingTimeNode msg_;
};

class Init_ProcessingTimeNode_id
{
public:
  Init_ProcessingTimeNode_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ProcessingTimeNode_name id(::autoware_internal_debug_msgs::msg::ProcessingTimeNode::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_ProcessingTimeNode_name(msg_);
  }

private:
  ::autoware_internal_debug_msgs::msg::ProcessingTimeNode msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_internal_debug_msgs::msg::ProcessingTimeNode>()
{
  return autoware_internal_debug_msgs::msg::builder::Init_ProcessingTimeNode_id();
}

}  // namespace autoware_internal_debug_msgs

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_NODE__BUILDER_HPP_
