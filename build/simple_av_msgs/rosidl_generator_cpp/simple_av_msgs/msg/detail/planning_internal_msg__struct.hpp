// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/PlanningInternalMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__PlanningInternalMsg __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__PlanningInternalMsg __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PlanningInternalMsg_
{
  using Type = PlanningInternalMsg_<ContainerAllocator>;

  explicit PlanningInternalMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_curve_detected = false;
      this->is_end_of_path = false;
    }
  }

  explicit PlanningInternalMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_curve_detected = false;
      this->is_end_of_path = false;
    }
  }

  // field types and members
  using _is_curve_detected_type =
    bool;
  _is_curve_detected_type is_curve_detected;
  using _is_end_of_path_type =
    bool;
  _is_end_of_path_type is_end_of_path;

  // setters for named parameter idiom
  Type & set__is_curve_detected(
    const bool & _arg)
  {
    this->is_curve_detected = _arg;
    return *this;
  }
  Type & set__is_end_of_path(
    const bool & _arg)
  {
    this->is_end_of_path = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__PlanningInternalMsg
    std::shared_ptr<simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__PlanningInternalMsg
    std::shared_ptr<simple_av_msgs::msg::PlanningInternalMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PlanningInternalMsg_ & other) const
  {
    if (this->is_curve_detected != other.is_curve_detected) {
      return false;
    }
    if (this->is_end_of_path != other.is_end_of_path) {
      return false;
    }
    return true;
  }
  bool operator!=(const PlanningInternalMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PlanningInternalMsg_

// alias to use template instance with default allocator
using PlanningInternalMsg =
  simple_av_msgs::msg::PlanningInternalMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MSG__STRUCT_HPP_
