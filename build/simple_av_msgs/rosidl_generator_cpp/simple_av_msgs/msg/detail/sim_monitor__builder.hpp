// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/SimMonitor.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/sim_monitor__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_SimMonitor_sim_clock_rate
{
public:
  explicit Init_SimMonitor_sim_clock_rate(::simple_av_msgs::msg::SimMonitor & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::SimMonitor sim_clock_rate(::simple_av_msgs::msg::SimMonitor::_sim_clock_rate_type arg)
  {
    msg_.sim_clock_rate = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::SimMonitor msg_;
};

class Init_SimMonitor_sim_time
{
public:
  explicit Init_SimMonitor_sim_time(::simple_av_msgs::msg::SimMonitor & msg)
  : msg_(msg)
  {}
  Init_SimMonitor_sim_clock_rate sim_time(::simple_av_msgs::msg::SimMonitor::_sim_time_type arg)
  {
    msg_.sim_time = std::move(arg);
    return Init_SimMonitor_sim_clock_rate(msg_);
  }

private:
  ::simple_av_msgs::msg::SimMonitor msg_;
};

class Init_SimMonitor_system_time
{
public:
  Init_SimMonitor_system_time()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SimMonitor_sim_time system_time(::simple_av_msgs::msg::SimMonitor::_system_time_type arg)
  {
    msg_.system_time = std::move(arg);
    return Init_SimMonitor_sim_time(msg_);
  }

private:
  ::simple_av_msgs::msg::SimMonitor msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::SimMonitor>()
{
  return simple_av_msgs::msg::builder::Init_SimMonitor_system_time();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__BUILDER_HPP_
