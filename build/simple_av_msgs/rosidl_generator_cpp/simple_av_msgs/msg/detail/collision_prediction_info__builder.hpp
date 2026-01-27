// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/CollisionPredictionInfo.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/collision_prediction_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_CollisionPredictionInfo_collision_detected
{
public:
  explicit Init_CollisionPredictionInfo_collision_detected(::simple_av_msgs::msg::CollisionPredictionInfo & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::CollisionPredictionInfo collision_detected(::simple_av_msgs::msg::CollisionPredictionInfo::_collision_detected_type arg)
  {
    msg_.collision_detected = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::CollisionPredictionInfo msg_;
};

class Init_CollisionPredictionInfo_object_velocity
{
public:
  explicit Init_CollisionPredictionInfo_object_velocity(::simple_av_msgs::msg::CollisionPredictionInfo & msg)
  : msg_(msg)
  {}
  Init_CollisionPredictionInfo_collision_detected object_velocity(::simple_av_msgs::msg::CollisionPredictionInfo::_object_velocity_type arg)
  {
    msg_.object_velocity = std::move(arg);
    return Init_CollisionPredictionInfo_collision_detected(msg_);
  }

private:
  ::simple_av_msgs::msg::CollisionPredictionInfo msg_;
};

class Init_CollisionPredictionInfo_object_label
{
public:
  explicit Init_CollisionPredictionInfo_object_label(::simple_av_msgs::msg::CollisionPredictionInfo & msg)
  : msg_(msg)
  {}
  Init_CollisionPredictionInfo_object_velocity object_label(::simple_av_msgs::msg::CollisionPredictionInfo::_object_label_type arg)
  {
    msg_.object_label = std::move(arg);
    return Init_CollisionPredictionInfo_object_velocity(msg_);
  }

private:
  ::simple_av_msgs::msg::CollisionPredictionInfo msg_;
};

class Init_CollisionPredictionInfo_time_to_collision
{
public:
  explicit Init_CollisionPredictionInfo_time_to_collision(::simple_av_msgs::msg::CollisionPredictionInfo & msg)
  : msg_(msg)
  {}
  Init_CollisionPredictionInfo_object_label time_to_collision(::simple_av_msgs::msg::CollisionPredictionInfo::_time_to_collision_type arg)
  {
    msg_.time_to_collision = std::move(arg);
    return Init_CollisionPredictionInfo_object_label(msg_);
  }

private:
  ::simple_av_msgs::msg::CollisionPredictionInfo msg_;
};

class Init_CollisionPredictionInfo_object_position
{
public:
  Init_CollisionPredictionInfo_object_position()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CollisionPredictionInfo_time_to_collision object_position(::simple_av_msgs::msg::CollisionPredictionInfo::_object_position_type arg)
  {
    msg_.object_position = std::move(arg);
    return Init_CollisionPredictionInfo_time_to_collision(msg_);
  }

private:
  ::simple_av_msgs::msg::CollisionPredictionInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::CollisionPredictionInfo>()
{
  return simple_av_msgs::msg::builder::Init_CollisionPredictionInfo_object_position();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__BUILDER_HPP_
