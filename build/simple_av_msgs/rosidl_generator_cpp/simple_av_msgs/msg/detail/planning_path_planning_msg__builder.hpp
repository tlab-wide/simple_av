// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/PlanningPathPlanningMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/planning_path_planning_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_PlanningPathPlanningMsg_speed_limit
{
public:
  explicit Init_PlanningPathPlanningMsg_speed_limit(::simple_av_msgs::msg::PlanningPathPlanningMsg & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::PlanningPathPlanningMsg speed_limit(::simple_av_msgs::msg::PlanningPathPlanningMsg::_speed_limit_type arg)
  {
    msg_.speed_limit = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningPathPlanningMsg msg_;
};

class Init_PlanningPathPlanningMsg_look_ahead_point
{
public:
  Init_PlanningPathPlanningMsg_look_ahead_point()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanningPathPlanningMsg_speed_limit look_ahead_point(::simple_av_msgs::msg::PlanningPathPlanningMsg::_look_ahead_point_type arg)
  {
    msg_.look_ahead_point = std::move(arg);
    return Init_PlanningPathPlanningMsg_speed_limit(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningPathPlanningMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::PlanningPathPlanningMsg>()
{
  return simple_av_msgs::msg::builder::Init_PlanningPathPlanningMsg_look_ahead_point();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__BUILDER_HPP_
