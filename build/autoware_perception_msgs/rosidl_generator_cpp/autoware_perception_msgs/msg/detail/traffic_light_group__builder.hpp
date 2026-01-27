// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_perception_msgs:msg/TrafficLightGroup.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP__BUILDER_HPP_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_perception_msgs/msg/detail/traffic_light_group__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_perception_msgs
{

namespace msg
{

namespace builder
{

class Init_TrafficLightGroup_predictions
{
public:
  explicit Init_TrafficLightGroup_predictions(::autoware_perception_msgs::msg::TrafficLightGroup & msg)
  : msg_(msg)
  {}
  ::autoware_perception_msgs::msg::TrafficLightGroup predictions(::autoware_perception_msgs::msg::TrafficLightGroup::_predictions_type arg)
  {
    msg_.predictions = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_perception_msgs::msg::TrafficLightGroup msg_;
};

class Init_TrafficLightGroup_elements
{
public:
  explicit Init_TrafficLightGroup_elements(::autoware_perception_msgs::msg::TrafficLightGroup & msg)
  : msg_(msg)
  {}
  Init_TrafficLightGroup_predictions elements(::autoware_perception_msgs::msg::TrafficLightGroup::_elements_type arg)
  {
    msg_.elements = std::move(arg);
    return Init_TrafficLightGroup_predictions(msg_);
  }

private:
  ::autoware_perception_msgs::msg::TrafficLightGroup msg_;
};

class Init_TrafficLightGroup_traffic_light_group_id
{
public:
  Init_TrafficLightGroup_traffic_light_group_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrafficLightGroup_elements traffic_light_group_id(::autoware_perception_msgs::msg::TrafficLightGroup::_traffic_light_group_id_type arg)
  {
    msg_.traffic_light_group_id = std::move(arg);
    return Init_TrafficLightGroup_elements(msg_);
  }

private:
  ::autoware_perception_msgs::msg::TrafficLightGroup msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_perception_msgs::msg::TrafficLightGroup>()
{
  return autoware_perception_msgs::msg::builder::Init_TrafficLightGroup_traffic_light_group_id();
}

}  // namespace autoware_perception_msgs

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP__BUILDER_HPP_
