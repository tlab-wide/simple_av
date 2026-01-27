// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:srv/TriggerMissionPlan.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__BUILDER_HPP_
#define SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/srv/detail/trigger_mission_plan__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::srv::TriggerMissionPlan_Request>()
{
  return ::simple_av_msgs::srv::TriggerMissionPlan_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace simple_av_msgs


namespace simple_av_msgs
{

namespace srv
{

namespace builder
{

class Init_TriggerMissionPlan_Response_message
{
public:
  explicit Init_TriggerMissionPlan_Response_message(::simple_av_msgs::srv::TriggerMissionPlan_Response & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::srv::TriggerMissionPlan_Response message(::simple_av_msgs::srv::TriggerMissionPlan_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::srv::TriggerMissionPlan_Response msg_;
};

class Init_TriggerMissionPlan_Response_success
{
public:
  Init_TriggerMissionPlan_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TriggerMissionPlan_Response_message success(::simple_av_msgs::srv::TriggerMissionPlan_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_TriggerMissionPlan_Response_message(msg_);
  }

private:
  ::simple_av_msgs::srv::TriggerMissionPlan_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::srv::TriggerMissionPlan_Response>()
{
  return simple_av_msgs::srv::builder::Init_TriggerMissionPlan_Response_success();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__BUILDER_HPP_
