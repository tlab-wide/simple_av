// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/PlanningWaypoint.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_WAYPOINT__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_WAYPOINT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/planning_waypoint__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_PlanningWaypoint_curve
{
public:
  explicit Init_PlanningWaypoint_curve(::simple_av_msgs::msg::PlanningWaypoint & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::PlanningWaypoint curve(::simple_av_msgs::msg::PlanningWaypoint::_curve_type arg)
  {
    msg_.curve = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningWaypoint msg_;
};

class Init_PlanningWaypoint_waypoint
{
public:
  Init_PlanningWaypoint_waypoint()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PlanningWaypoint_curve waypoint(::simple_av_msgs::msg::PlanningWaypoint::_waypoint_type arg)
  {
    msg_.waypoint = std::move(arg);
    return Init_PlanningWaypoint_curve(msg_);
  }

private:
  ::simple_av_msgs::msg::PlanningWaypoint msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::PlanningWaypoint>()
{
  return simple_av_msgs::msg::builder::Init_PlanningWaypoint_waypoint();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_WAYPOINT__BUILDER_HPP_
