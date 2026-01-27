// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_perception_msgs:msg/PredictedTrafficLightState.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__BUILDER_HPP_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_perception_msgs/msg/detail/predicted_traffic_light_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_perception_msgs
{

namespace msg
{

namespace builder
{

class Init_PredictedTrafficLightState_information_source
{
public:
  explicit Init_PredictedTrafficLightState_information_source(::autoware_perception_msgs::msg::PredictedTrafficLightState & msg)
  : msg_(msg)
  {}
  ::autoware_perception_msgs::msg::PredictedTrafficLightState information_source(::autoware_perception_msgs::msg::PredictedTrafficLightState::_information_source_type arg)
  {
    msg_.information_source = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_perception_msgs::msg::PredictedTrafficLightState msg_;
};

class Init_PredictedTrafficLightState_reliability
{
public:
  explicit Init_PredictedTrafficLightState_reliability(::autoware_perception_msgs::msg::PredictedTrafficLightState & msg)
  : msg_(msg)
  {}
  Init_PredictedTrafficLightState_information_source reliability(::autoware_perception_msgs::msg::PredictedTrafficLightState::_reliability_type arg)
  {
    msg_.reliability = std::move(arg);
    return Init_PredictedTrafficLightState_information_source(msg_);
  }

private:
  ::autoware_perception_msgs::msg::PredictedTrafficLightState msg_;
};

class Init_PredictedTrafficLightState_simultaneous_elements
{
public:
  explicit Init_PredictedTrafficLightState_simultaneous_elements(::autoware_perception_msgs::msg::PredictedTrafficLightState & msg)
  : msg_(msg)
  {}
  Init_PredictedTrafficLightState_reliability simultaneous_elements(::autoware_perception_msgs::msg::PredictedTrafficLightState::_simultaneous_elements_type arg)
  {
    msg_.simultaneous_elements = std::move(arg);
    return Init_PredictedTrafficLightState_reliability(msg_);
  }

private:
  ::autoware_perception_msgs::msg::PredictedTrafficLightState msg_;
};

class Init_PredictedTrafficLightState_predicted_stamp
{
public:
  Init_PredictedTrafficLightState_predicted_stamp()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PredictedTrafficLightState_simultaneous_elements predicted_stamp(::autoware_perception_msgs::msg::PredictedTrafficLightState::_predicted_stamp_type arg)
  {
    msg_.predicted_stamp = std::move(arg);
    return Init_PredictedTrafficLightState_simultaneous_elements(msg_);
  }

private:
  ::autoware_perception_msgs::msg::PredictedTrafficLightState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_perception_msgs::msg::PredictedTrafficLightState>()
{
  return autoware_perception_msgs::msg::builder::Init_PredictedTrafficLightState_predicted_stamp();
}

}  // namespace autoware_perception_msgs

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__BUILDER_HPP_
