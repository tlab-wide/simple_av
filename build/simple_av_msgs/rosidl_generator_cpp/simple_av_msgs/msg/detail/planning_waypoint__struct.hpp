// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/PlanningWaypoint.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_WAYPOINT__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_WAYPOINT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'waypoint'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__PlanningWaypoint __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__PlanningWaypoint __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PlanningWaypoint_
{
  using Type = PlanningWaypoint_<ContainerAllocator>;

  explicit PlanningWaypoint_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : waypoint(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->curve = 0.0f;
    }
  }

  explicit PlanningWaypoint_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : waypoint(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->curve = 0.0f;
    }
  }

  // field types and members
  using _waypoint_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _waypoint_type waypoint;
  using _curve_type =
    float;
  _curve_type curve;

  // setters for named parameter idiom
  Type & set__waypoint(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->waypoint = _arg;
    return *this;
  }
  Type & set__curve(
    const float & _arg)
  {
    this->curve = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__PlanningWaypoint
    std::shared_ptr<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__PlanningWaypoint
    std::shared_ptr<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PlanningWaypoint_ & other) const
  {
    if (this->waypoint != other.waypoint) {
      return false;
    }
    if (this->curve != other.curve) {
      return false;
    }
    return true;
  }
  bool operator!=(const PlanningWaypoint_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PlanningWaypoint_

// alias to use template instance with default allocator
using PlanningWaypoint =
  simple_av_msgs::msg::PlanningWaypoint_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_WAYPOINT__STRUCT_HPP_
