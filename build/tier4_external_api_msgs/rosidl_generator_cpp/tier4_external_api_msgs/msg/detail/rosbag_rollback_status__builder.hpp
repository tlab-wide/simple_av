// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from tier4_external_api_msgs:msg/RosbagRollbackStatus.idl
// generated code does not contain a copyright notice

#ifndef TIER4_EXTERNAL_API_MSGS__MSG__DETAIL__ROSBAG_ROLLBACK_STATUS__BUILDER_HPP_
#define TIER4_EXTERNAL_API_MSGS__MSG__DETAIL__ROSBAG_ROLLBACK_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "tier4_external_api_msgs/msg/detail/rosbag_rollback_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace tier4_external_api_msgs
{

namespace msg
{

namespace builder
{

class Init_RosbagRollbackStatus_remaining_time
{
public:
  explicit Init_RosbagRollbackStatus_remaining_time(::tier4_external_api_msgs::msg::RosbagRollbackStatus & msg)
  : msg_(msg)
  {}
  ::tier4_external_api_msgs::msg::RosbagRollbackStatus remaining_time(::tier4_external_api_msgs::msg::RosbagRollbackStatus::_remaining_time_type arg)
  {
    msg_.remaining_time = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRollbackStatus msg_;
};

class Init_RosbagRollbackStatus_estimated_time
{
public:
  explicit Init_RosbagRollbackStatus_estimated_time(::tier4_external_api_msgs::msg::RosbagRollbackStatus & msg)
  : msg_(msg)
  {}
  Init_RosbagRollbackStatus_remaining_time estimated_time(::tier4_external_api_msgs::msg::RosbagRollbackStatus::_estimated_time_type arg)
  {
    msg_.estimated_time = std::move(arg);
    return Init_RosbagRollbackStatus_remaining_time(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRollbackStatus msg_;
};

class Init_RosbagRollbackStatus_elapsed_time
{
public:
  explicit Init_RosbagRollbackStatus_elapsed_time(::tier4_external_api_msgs::msg::RosbagRollbackStatus & msg)
  : msg_(msg)
  {}
  Init_RosbagRollbackStatus_estimated_time elapsed_time(::tier4_external_api_msgs::msg::RosbagRollbackStatus::_elapsed_time_type arg)
  {
    msg_.elapsed_time = std::move(arg);
    return Init_RosbagRollbackStatus_estimated_time(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRollbackStatus msg_;
};

class Init_RosbagRollbackStatus_bytes_copied
{
public:
  explicit Init_RosbagRollbackStatus_bytes_copied(::tier4_external_api_msgs::msg::RosbagRollbackStatus & msg)
  : msg_(msg)
  {}
  Init_RosbagRollbackStatus_elapsed_time bytes_copied(::tier4_external_api_msgs::msg::RosbagRollbackStatus::_bytes_copied_type arg)
  {
    msg_.bytes_copied = std::move(arg);
    return Init_RosbagRollbackStatus_elapsed_time(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRollbackStatus msg_;
};

class Init_RosbagRollbackStatus_bytes_to_copy
{
public:
  explicit Init_RosbagRollbackStatus_bytes_to_copy(::tier4_external_api_msgs::msg::RosbagRollbackStatus & msg)
  : msg_(msg)
  {}
  Init_RosbagRollbackStatus_bytes_copied bytes_to_copy(::tier4_external_api_msgs::msg::RosbagRollbackStatus::_bytes_to_copy_type arg)
  {
    msg_.bytes_to_copy = std::move(arg);
    return Init_RosbagRollbackStatus_bytes_copied(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRollbackStatus msg_;
};

class Init_RosbagRollbackStatus_progress
{
public:
  explicit Init_RosbagRollbackStatus_progress(::tier4_external_api_msgs::msg::RosbagRollbackStatus & msg)
  : msg_(msg)
  {}
  Init_RosbagRollbackStatus_bytes_to_copy progress(::tier4_external_api_msgs::msg::RosbagRollbackStatus::_progress_type arg)
  {
    msg_.progress = std::move(arg);
    return Init_RosbagRollbackStatus_bytes_to_copy(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRollbackStatus msg_;
};

class Init_RosbagRollbackStatus_message
{
public:
  explicit Init_RosbagRollbackStatus_message(::tier4_external_api_msgs::msg::RosbagRollbackStatus & msg)
  : msg_(msg)
  {}
  Init_RosbagRollbackStatus_progress message(::tier4_external_api_msgs::msg::RosbagRollbackStatus::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_RosbagRollbackStatus_progress(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRollbackStatus msg_;
};

class Init_RosbagRollbackStatus_status
{
public:
  Init_RosbagRollbackStatus_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_RosbagRollbackStatus_message status(::tier4_external_api_msgs::msg::RosbagRollbackStatus::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_RosbagRollbackStatus_message(msg_);
  }

private:
  ::tier4_external_api_msgs::msg::RosbagRollbackStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::tier4_external_api_msgs::msg::RosbagRollbackStatus>()
{
  return tier4_external_api_msgs::msg::builder::Init_RosbagRollbackStatus_status();
}

}  // namespace tier4_external_api_msgs

#endif  // TIER4_EXTERNAL_API_MSGS__MSG__DETAIL__ROSBAG_ROLLBACK_STATUS__BUILDER_HPP_
