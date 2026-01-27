// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_internal_metric_msgs:msg/Metric.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__BUILDER_HPP_
#define AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_internal_metric_msgs/msg/detail/metric__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_internal_metric_msgs
{

namespace msg
{

namespace builder
{

class Init_Metric_value
{
public:
  explicit Init_Metric_value(::autoware_internal_metric_msgs::msg::Metric & msg)
  : msg_(msg)
  {}
  ::autoware_internal_metric_msgs::msg::Metric value(::autoware_internal_metric_msgs::msg::Metric::_value_type arg)
  {
    msg_.value = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_internal_metric_msgs::msg::Metric msg_;
};

class Init_Metric_unit
{
public:
  explicit Init_Metric_unit(::autoware_internal_metric_msgs::msg::Metric & msg)
  : msg_(msg)
  {}
  Init_Metric_value unit(::autoware_internal_metric_msgs::msg::Metric::_unit_type arg)
  {
    msg_.unit = std::move(arg);
    return Init_Metric_value(msg_);
  }

private:
  ::autoware_internal_metric_msgs::msg::Metric msg_;
};

class Init_Metric_name
{
public:
  Init_Metric_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Metric_unit name(::autoware_internal_metric_msgs::msg::Metric::_name_type arg)
  {
    msg_.name = std::move(arg);
    return Init_Metric_unit(msg_);
  }

private:
  ::autoware_internal_metric_msgs::msg::Metric msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_internal_metric_msgs::msg::Metric>()
{
  return autoware_internal_metric_msgs::msg::builder::Init_Metric_name();
}

}  // namespace autoware_internal_metric_msgs

#endif  // AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__BUILDER_HPP_
