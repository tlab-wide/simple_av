// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_internal_metric_msgs:msg/MetricArray.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__BUILDER_HPP_
#define AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_internal_metric_msgs/msg/detail/metric_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_internal_metric_msgs
{

namespace msg
{

namespace builder
{

class Init_MetricArray_metric_array
{
public:
  explicit Init_MetricArray_metric_array(::autoware_internal_metric_msgs::msg::MetricArray & msg)
  : msg_(msg)
  {}
  ::autoware_internal_metric_msgs::msg::MetricArray metric_array(::autoware_internal_metric_msgs::msg::MetricArray::_metric_array_type arg)
  {
    msg_.metric_array = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_internal_metric_msgs::msg::MetricArray msg_;
};

class Init_MetricArray_stamp
{
public:
  Init_MetricArray_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MetricArray_metric_array stamp(::autoware_internal_metric_msgs::msg::MetricArray::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_MetricArray_metric_array(msg_);
  }

private:
  ::autoware_internal_metric_msgs::msg::MetricArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_internal_metric_msgs::msg::MetricArray>()
{
  return autoware_internal_metric_msgs::msg::builder::Init_MetricArray_stamp();
}

}  // namespace autoware_internal_metric_msgs

#endif  // AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__BUILDER_HPP_
