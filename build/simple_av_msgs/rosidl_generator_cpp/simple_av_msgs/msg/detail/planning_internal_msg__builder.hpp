// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/PlanningInternalMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/planning_internal_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_PlanningInternalMsg_is_end_of_path
{
public:
  explicit Init_PlanningInternalMsg_is_end_of_path(::simple_av_msgs::msg::PlanningInternalMsg & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::PlanningInternalMsg is_end_of_path(::simple_av_msgs::msg::PlanningInternalMsg::_is_end_of_path_type arg)
  {
    msg_.is_end_of_path = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningInternalMsg msg_;
};

class Init_PlanningInternalMsg_is_curve_detected
{
public:
  Init_PlanningInternalMsg_is_curve_detected()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanningInternalMsg_is_end_of_path is_curve_detected(::simple_av_msgs::msg::PlanningInternalMsg::_is_curve_detected_type arg)
  {
    msg_.is_curve_detected = std::move(arg);
    return Init_PlanningInternalMsg_is_end_of_path(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningInternalMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::PlanningInternalMsg>()
{
  return simple_av_msgs::msg::builder::Init_PlanningInternalMsg_is_curve_detected();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__BUILDER_HPP_
