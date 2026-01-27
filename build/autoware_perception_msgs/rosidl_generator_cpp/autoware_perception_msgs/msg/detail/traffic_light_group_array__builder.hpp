// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_perception_msgs:msg/TrafficLightGroupArray.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP_ARRAY__BUILDER_HPP_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_perception_msgs/msg/detail/traffic_light_group_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_perception_msgs
{

namespace msg
{

namespace builder
{

class Init_TrafficLightGroupArray_traffic_light_groups
{
public:
  explicit Init_TrafficLightGroupArray_traffic_light_groups(::autoware_perception_msgs::msg::TrafficLightGroupArray & msg)
  : msg_(msg)
  {}
  ::autoware_perception_msgs::msg::TrafficLightGroupArray traffic_light_groups(::autoware_perception_msgs::msg::TrafficLightGroupArray::_traffic_light_groups_type arg)
  {
    msg_.traffic_light_groups = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_perception_msgs::msg::TrafficLightGroupArray msg_;
};

class Init_TrafficLightGroupArray_stamp
{
public:
  Init_TrafficLightGroupArray_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrafficLightGroupArray_traffic_light_groups stamp(::autoware_perception_msgs::msg::TrafficLightGroupArray::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return Init_TrafficLightGroupArray_traffic_light_groups(msg_);
  }

private:
  ::autoware_perception_msgs::msg::TrafficLightGroupArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_perception_msgs::msg::TrafficLightGroupArray>()
{
  return autoware_perception_msgs::msg::builder::Init_TrafficLightGroupArray_stamp();
}

}  // namespace autoware_perception_msgs

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP_ARRAY__BUILDER_HPP_
