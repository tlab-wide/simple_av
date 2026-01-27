// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/DetectedObject.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/detected_object__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_DetectedObject_nearest_object_side
{
public:
  explicit Init_DetectedObject_nearest_object_side(::simple_av_msgs::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  ::simple_av_msgs::msg::DetectedObject nearest_object_side(::simple_av_msgs::msg::DetectedObject::_nearest_object_side_type arg)
  {
    msg_.nearest_object_side = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

class Init_DetectedObject_distance
{
public:
  explicit Init_DetectedObject_distance(::simple_av_msgs::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_nearest_object_side distance(::simple_av_msgs::msg::DetectedObject::_distance_type arg)
  {
    msg_.distance = std::move(arg);
    return Init_DetectedObject_nearest_object_side(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

class Init_DetectedObject_bounding_box
{
public:
  explicit Init_DetectedObject_bounding_box(::simple_av_msgs::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_distance bounding_box(::simple_av_msgs::msg::DetectedObject::_bounding_box_type arg)
  {
    msg_.bounding_box = std::move(arg);
    return Init_DetectedObject_distance(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

class Init_DetectedObject_relative_direction
{
public:
  explicit Init_DetectedObject_relative_direction(::simple_av_msgs::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_bounding_box relative_direction(::simple_av_msgs::msg::DetectedObject::_relative_direction_type arg)
  {
    msg_.relative_direction = std::move(arg);
    return Init_DetectedObject_bounding_box(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

class Init_DetectedObject_shape
{
public:
  explicit Init_DetectedObject_shape(::simple_av_msgs::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_relative_direction shape(::simple_av_msgs::msg::DetectedObject::_shape_type arg)
  {
    msg_.shape = std::move(arg);
    return Init_DetectedObject_relative_direction(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

class Init_DetectedObject_orientation
{
public:
  explicit Init_DetectedObject_orientation(::simple_av_msgs::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_shape orientation(::simple_av_msgs::msg::DetectedObject::_orientation_type arg)
  {
    msg_.orientation = std::move(arg);
    return Init_DetectedObject_shape(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

class Init_DetectedObject_velocity
{
public:
  explicit Init_DetectedObject_velocity(::simple_av_msgs::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_orientation velocity(::simple_av_msgs::msg::DetectedObject::_velocity_type arg)
  {
    msg_.velocity = std::move(arg);
    return Init_DetectedObject_orientation(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

class Init_DetectedObject_position
{
public:
  explicit Init_DetectedObject_position(::simple_av_msgs::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_velocity position(::simple_av_msgs::msg::DetectedObject::_position_type arg)
  {
    msg_.position = std::move(arg);
    return Init_DetectedObject_velocity(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

class Init_DetectedObject_label
{
public:
  explicit Init_DetectedObject_label(::simple_av_msgs::msg::DetectedObject & msg)
  : msg_(msg)
  {}
  Init_DetectedObject_position label(::simple_av_msgs::msg::DetectedObject::_label_type arg)
  {
    msg_.label = std::move(arg);
    return Init_DetectedObject_position(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

class Init_DetectedObject_is_from_rsu
{
public:
  Init_DetectedObject_is_from_rsu()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_DetectedObject_label is_from_rsu(::simple_av_msgs::msg::DetectedObject::_is_from_rsu_type arg)
  {
    msg_.is_from_rsu = std::move(arg);
    return Init_DetectedObject_label(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObject msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::DetectedObject>()
{
  return simple_av_msgs::msg::builder::Init_DetectedObject_is_from_rsu();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__BUILDER_HPP_
