// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from simple_av_msgs:msg/DetectedObjectsArray.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECTS_ARRAY__BUILDER_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECTS_ARRAY__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "simple_av_msgs/msg/detail/detected_objects_array__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace simple_av_msgs
{

namespace msg
{

namespace builder
{

class Init_DetectedObjectsArray_objects
{
public:
  Init_DetectedObjectsArray_objects()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::simple_av_msgs::msg::DetectedObjectsArray objects(::simple_av_msgs::msg::DetectedObjectsArray::_objects_type arg)
  {
    msg_.objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::simple_av_msgs::msg::DetectedObjectsArray msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::simple_av_msgs::msg::DetectedObjectsArray>()
{
  return simple_av_msgs::msg::builder::Init_DetectedObjectsArray_objects();
}

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECTS_ARRAY__BUILDER_HPP_
