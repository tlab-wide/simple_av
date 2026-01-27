// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_perception_msgs:msg/TrafficLightElement.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_ELEMENT__BUILDER_HPP_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_ELEMENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_perception_msgs/msg/detail/traffic_light_element__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_perception_msgs
{

namespace msg
{

namespace builder
{

class Init_TrafficLightElement_confidence
{
public:
  explicit Init_TrafficLightElement_confidence(::autoware_perception_msgs::msg::TrafficLightElement & msg)
  : msg_(msg)
  {}
  ::autoware_perception_msgs::msg::TrafficLightElement confidence(::autoware_perception_msgs::msg::TrafficLightElement::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_perception_msgs::msg::TrafficLightElement msg_;
};

class Init_TrafficLightElement_status
{
public:
  explicit Init_TrafficLightElement_status(::autoware_perception_msgs::msg::TrafficLightElement & msg)
  : msg_(msg)
  {}
  Init_TrafficLightElement_confidence status(::autoware_perception_msgs::msg::TrafficLightElement::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_TrafficLightElement_confidence(msg_);
  }

private:
  ::autoware_perception_msgs::msg::TrafficLightElement msg_;
};

class Init_TrafficLightElement_shape
{
public:
  explicit Init_TrafficLightElement_shape(::autoware_perception_msgs::msg::TrafficLightElement & msg)
  : msg_(msg)
  {}
  Init_TrafficLightElement_status shape(::autoware_perception_msgs::msg::TrafficLightElement::_shape_type arg)
  {
    msg_.shape = std::move(arg);
    return Init_TrafficLightElement_status(msg_);
  }

private:
  ::autoware_perception_msgs::msg::TrafficLightElement msg_;
};

class Init_TrafficLightElement_color
{
public:
  Init_TrafficLightElement_color()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_TrafficLightElement_shape color(::autoware_perception_msgs::msg::TrafficLightElement::_color_type arg)
  {
    msg_.color = std::move(arg);
    return Init_TrafficLightElement_shape(msg_);
  }

private:
  ::autoware_perception_msgs::msg::TrafficLightElement msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_perception_msgs::msg::TrafficLightElement>()
{
  return autoware_perception_msgs::msg::builder::Init_TrafficLightElement_color();
}

}  // namespace autoware_perception_msgs

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_ELEMENT__BUILDER_HPP_
