// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from tier4_external_api_msgs:msg/RosbagRecordStatus.idl
// generated code does not contain a copyright notice

#ifndef TIER4_EXTERNAL_API_MSGS__MSG__DETAIL__ROSBAG_RECORD_STATUS__BUILDER_HPP_
#define TIER4_EXTERNAL_API_MSGS__MSG__DETAIL__ROSBAG_RECORD_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "tier4_external_api_msgs/msg/detail/rosbag_record_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace tier4_external_api_msgs
{

namespace msg
{

namespace builder
{

class Init_RosbagRecordStatus_message
{
public:
  explicit Init_RosbagRecordStatus_message(::tier4_external_api_msgs::msg::RosbagRecordStatus & msg)
  : msg_(msg)
  {}
  ::tier4_external_api_msgs::msg::RosbagRecordStatus message(::tier4_external_api_msgs::msg::RosbagRecordStatus::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRecordStatus msg_;
};

class Init_RosbagRecordStatus_status
{
public:
  Init_RosbagRecordStatus_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RosbagRecordStatus_message status(::tier4_external_api_msgs::msg::RosbagRecordStatus::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_RosbagRecordStatus_message(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRecordStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::tier4_external_api_msgs::msg::RosbagRecordStatus>()
{
  return tier4_external_api_msgs::msg::builder::Init_RosbagRecordStatus_status();
}

}  // namespace tier4_external_api_msgs

#endif  // TIER4_EXTERNAL_API_MSGS__MSG__DETAIL__ROSBAG_RECORD_STATUS__BUILDER_HPP_
