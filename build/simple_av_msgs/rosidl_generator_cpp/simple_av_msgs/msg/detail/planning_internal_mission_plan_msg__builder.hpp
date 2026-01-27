// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/PlanningInternalMissionPlanMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/planning_internal_mission_plan_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_PlanningInternalMissionPlanMsg_path_as_lanes
{
public:
  explicit Init_PlanningInternalMissionPlanMsg_path_as_lanes(::simple_av_msgs::msg::PlanningInternalMissionPlanMsg & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::PlanningInternalMissionPlanMsg path_as_lanes(::simple_av_msgs::msg::PlanningInternalMissionPlanMsg::_path_as_lanes_type arg)
  {
    msg_.path_as_lanes = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningInternalMissionPlanMsg msg_;
};

class Init_PlanningInternalMissionPlanMsg_path
{
public:
  Init_PlanningInternalMissionPlanMsg_path()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanningInternalMissionPlanMsg_path_as_lanes path(::simple_av_msgs::msg::PlanningInternalMissionPlanMsg::_path_type arg)
  {
    msg_.path = std::move(arg);
    return Init_PlanningInternalMissionPlanMsg_path_as_lanes(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningInternalMissionPlanMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::PlanningInternalMissionPlanMsg>()
{
  return simple_av_msgs::msg::builder::Init_PlanningInternalMissionPlanMsg_path();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__BUILDER_HPP_
