// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/PlanningMotionPlanningMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/planning_motion_planning_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_PlanningMotionPlanningMsg_stop_reason
{
public:
  explicit Init_PlanningMotionPlanningMsg_stop_reason(::simple_av_msgs::msg::PlanningMotionPlanningMsg & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::PlanningMotionPlanningMsg stop_reason(::simple_av_msgs::msg::PlanningMotionPlanningMsg::_stop_reason_type arg)
  {
    msg_.stop_reason = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningMotionPlanningMsg msg_;
};

class Init_PlanningMotionPlanningMsg_status
{
public:
  explicit Init_PlanningMotionPlanningMsg_status(::simple_av_msgs::msg::PlanningMotionPlanningMsg & msg)
  : msg_(msg)
  {}
  Init_PlanningMotionPlanningMsg_stop_reason status(::simple_av_msgs::msg::PlanningMotionPlanningMsg::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_PlanningMotionPlanningMsg_stop_reason(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningMotionPlanningMsg msg_;
};

class Init_PlanningMotionPlanningMsg_stop_point
{
public:
  Init_PlanningMotionPlanningMsg_stop_point()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanningMotionPlanningMsg_status stop_point(::simple_av_msgs::msg::PlanningMotionPlanningMsg::_stop_point_type arg)
  {
    msg_.stop_point = std::move(arg);
    return Init_PlanningMotionPlanningMsg_status(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningMotionPlanningMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::PlanningMotionPlanningMsg>()
{
  return simple_av_msgs::msg::builder::Init_PlanningMotionPlanningMsg_stop_point();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__BUILDER_HPP_
