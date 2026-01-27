// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/PlanningMotionPlanningMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'stop_point'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'status'
// Member 'stop_reason'
#include "std_msgs/msg/detail/string__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__PlanningMotionPlanningMsg __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__PlanningMotionPlanningMsg __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PlanningMotionPlanningMsg_
{
  using Type = PlanningMotionPlanningMsg_<ContainerAllocator>;

  explicit PlanningMotionPlanningMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stop_point(_init),
    status(_init),
    stop_reason(_init)
  {
    (void)_init;
  }

  explicit PlanningMotionPlanningMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stop_point(_alloc, _init),
    status(_alloc, _init),
    stop_reason(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _stop_point_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _stop_point_type stop_point;
  using _status_type =
    std_msgs::msg::String_<ContainerAllocator>;
  _status_type status;
  using _stop_reason_type =
    std_msgs::msg::String_<ContainerAllocator>;
  _stop_reason_type stop_reason;

  // setters for named parameter idiom
  Type & set__stop_point(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->stop_point = _arg;
    return *this;
  }
  Type & set__status(
    const std_msgs::msg::String_<ContainerAllocator> & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__stop_reason(
    const std_msgs::msg::String_<ContainerAllocator> & _arg)
  {
    this->stop_reason = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__PlanningMotionPlanningMsg
    std::shared_ptr<simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__PlanningMotionPlanningMsg
    std::shared_ptr<simple_av_msgs::msg::PlanningMotionPlanningMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PlanningMotionPlanningMsg_ & other) const
  {
    if (this->stop_point != other.stop_point) {
      return false;
    }
    if (this->status != other.status) {
      return false;
    }
    if (this->stop_reason != other.stop_reason) {
      return false;
    }
    return true;
  }
  bool operator!=(const PlanningMotionPlanningMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PlanningMotionPlanningMsg_

// alias to use template instance with default allocator
using PlanningMotionPlanningMsg =
  simple_av_msgs::msg::PlanningMotionPlanningMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_MOTION_PLANNING_MSG__STRUCT_HPP_
