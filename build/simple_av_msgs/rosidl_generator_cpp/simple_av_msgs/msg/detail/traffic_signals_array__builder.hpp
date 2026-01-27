// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/TrafficSignalsArray.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/traffic_signals_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_TrafficSignalsArray_v2i_traffic_signals_colors
{
public:
  explicit Init_TrafficSignalsArray_v2i_traffic_signals_colors(::simple_av_msgs::msg::TrafficSignalsArray & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::TrafficSignalsArray v2i_traffic_signals_colors(::simple_av_msgs::msg::TrafficSignalsArray::_v2i_traffic_signals_colors_type arg)
  {
    msg_.v2i_traffic_signals_colors = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::TrafficSignalsArray msg_;
};

class Init_TrafficSignalsArray_v2i_traffic_signals_id
{
public:
  Init_TrafficSignalsArray_v2i_traffic_signals_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrafficSignalsArray_v2i_traffic_signals_colors v2i_traffic_signals_id(::simple_av_msgs::msg::TrafficSignalsArray::_v2i_traffic_signals_id_type arg)
  {
    msg_.v2i_traffic_signals_id = std::move(arg);
    return Init_TrafficSignalsArray_v2i_traffic_signals_colors(msg_);
  }

private:
  ::simple_av_msgs::msg::TrafficSignalsArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::TrafficSignalsArray>()
{
  return simple_av_msgs::msg::builder::Init_TrafficSignalsArray_v2i_traffic_signals_id();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__BUILDER_HPP_
