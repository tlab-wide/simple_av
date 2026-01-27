// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/LocalizationMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/localization_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_LocalizationMsg_minimal_distance
{
public:
  explicit Init_LocalizationMsg_minimal_distance(::simple_av_msgs::msg::LocalizationMsg & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::LocalizationMsg minimal_distance(::simple_av_msgs::msg::LocalizationMsg::_minimal_distance_type arg)
  {
    msg_.minimal_distance = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::LocalizationMsg msg_;
};

class Init_LocalizationMsg_closest_lane_names
{
public:
  explicit Init_LocalizationMsg_closest_lane_names(::simple_av_msgs::msg::LocalizationMsg & msg)
  : msg_(msg)
  {}
  Init_LocalizationMsg_minimal_distance closest_lane_names(::simple_av_msgs::msg::LocalizationMsg::_closest_lane_names_type arg)
  {
    msg_.closest_lane_names = std::move(arg);
    return Init_LocalizationMsg_minimal_distance(msg_);
  }

private:
  ::simple_av_msgs::msg::LocalizationMsg msg_;
};

class Init_LocalizationMsg_closest_point
{
public:
  Init_LocalizationMsg_closest_point()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LocalizationMsg_closest_lane_names closest_point(::simple_av_msgs::msg::LocalizationMsg::_closest_point_type arg)
  {
    msg_.closest_point = std::move(arg);
    return Init_LocalizationMsg_closest_lane_names(msg_);
  }

private:
  ::simple_av_msgs::msg::LocalizationMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::LocalizationMsg>()
{
  return simple_av_msgs::msg::builder::Init_LocalizationMsg_closest_point();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__BUILDER_HPP_
