// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/Portal.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/portal__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_Portal_finished
{
public:
  explicit Init_Portal_finished(::simple_av_msgs::msg::Portal & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::Portal finished(::simple_av_msgs::msg::Portal::_finished_type arg)
  {
    msg_.finished = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::Portal msg_;
};

class Init_Portal_round_number
{
public:
  explicit Init_Portal_round_number(::simple_av_msgs::msg::Portal & msg)
  : msg_(msg)
  {}
  Init_Portal_finished round_number(::simple_av_msgs::msg::Portal::_round_number_type arg)
  {
    msg_.round_number = std::move(arg);
    return Init_Portal_finished(msg_);
  }

private:
  ::simple_av_msgs::msg::Portal msg_;
};

class Init_Portal_reset
{
public:
  Init_Portal_reset()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Portal_round_number reset(::simple_av_msgs::msg::Portal::_reset_type arg)
  {
    msg_.reset = std::move(arg);
    return Init_Portal_round_number(msg_);
  }

private:
  ::simple_av_msgs::msg::Portal msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::Portal>()
{
  return simple_av_msgs::msg::builder::Init_Portal_reset();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__BUILDER_HPP_
