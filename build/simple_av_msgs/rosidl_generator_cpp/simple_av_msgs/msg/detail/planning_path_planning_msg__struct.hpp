// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/PlanningPathPlanningMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'look_ahead_point'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__PlanningPathPlanningMsg __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__PlanningPathPlanningMsg __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PlanningPathPlanningMsg_
{
  using Type = PlanningPathPlanningMsg_<ContainerAllocator>;

  explicit PlanningPathPlanningMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : look_ahead_point(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->speed_limit = 0.0;
    }
  }

  explicit PlanningPathPlanningMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : look_ahead_point(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->speed_limit = 0.0;
    }
  }

  // field types and members
  using _look_ahead_point_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _look_ahead_point_type look_ahead_point;
  using _speed_limit_type =
    double;
  _speed_limit_type speed_limit;

  // setters for named parameter idiom
  Type & set__look_ahead_point(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->look_ahead_point = _arg;
    return *this;
  }
  Type & set__speed_limit(
    const double & _arg)
  {
    this->speed_limit = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__PlanningPathPlanningMsg
    std::shared_ptr<simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__PlanningPathPlanningMsg
    std::shared_ptr<simple_av_msgs::msg::PlanningPathPlanningMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PlanningPathPlanningMsg_ & other) const
  {
    if (this->look_ahead_point != other.look_ahead_point) {
      return false;
    }
    if (this->speed_limit != other.speed_limit) {
      return false;
    }
    return true;
  }
  bool operator!=(const PlanningPathPlanningMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PlanningPathPlanningMsg_

// alias to use template instance with default allocator
using PlanningPathPlanningMsg =
  simple_av_msgs::msg::PlanningPathPlanningMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_PATH_PLANNING_MSG__STRUCT_HPP_
