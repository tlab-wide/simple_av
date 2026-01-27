// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/LocalizationIntersectionStatus.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/localization_intersection_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_LocalizationIntersectionStatus_distance_to_intersection
{
public:
  explicit Init_LocalizationIntersectionStatus_distance_to_intersection(::simple_av_msgs::msg::LocalizationIntersectionStatus & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::LocalizationIntersectionStatus distance_to_intersection(::simple_av_msgs::msg::LocalizationIntersectionStatus::_distance_to_intersection_type arg)
  {
    msg_.distance_to_intersection = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::LocalizationIntersectionStatus msg_;
};

class Init_LocalizationIntersectionStatus_status
{
public:
  explicit Init_LocalizationIntersectionStatus_status(::simple_av_msgs::msg::LocalizationIntersectionStatus & msg)
  : msg_(msg)
  {}
  Init_LocalizationIntersectionStatus_distance_to_intersection status(::simple_av_msgs::msg::LocalizationIntersectionStatus::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_LocalizationIntersectionStatus_distance_to_intersection(msg_);
  }

private:
  ::simple_av_msgs::msg::LocalizationIntersectionStatus msg_;
};

class Init_LocalizationIntersectionStatus_intersection_name
{
public:
  Init_LocalizationIntersectionStatus_intersection_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LocalizationIntersectionStatus_status intersection_name(::simple_av_msgs::msg::LocalizationIntersectionStatus::_intersection_name_type arg)
  {
    msg_.intersection_name = std::move(arg);
    return Init_LocalizationIntersectionStatus_status(msg_);
  }

private:
  ::simple_av_msgs::msg::LocalizationIntersectionStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::LocalizationIntersectionStatus>()
{
  return simple_av_msgs::msg::builder::Init_LocalizationIntersectionStatus_intersection_name();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__BUILDER_HPP_
