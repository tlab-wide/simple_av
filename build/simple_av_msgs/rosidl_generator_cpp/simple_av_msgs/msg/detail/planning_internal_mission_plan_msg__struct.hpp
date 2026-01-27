// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/PlanningInternalMissionPlanMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'path'
#include "simple_av_msgs/msg/detail/planning_waypoint__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__PlanningInternalMissionPlanMsg __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__PlanningInternalMissionPlanMsg __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PlanningInternalMissionPlanMsg_
{
  using Type = PlanningInternalMissionPlanMsg_<ContainerAllocator>;

  explicit PlanningInternalMissionPlanMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit PlanningInternalMissionPlanMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _path_type =
    std::vector<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>>>;
  _path_type path;
  using _path_as_lanes_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _path_as_lanes_type path_as_lanes;

  // setters for named parameter idiom
  Type & set__path(
    const std::vector<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<simple_av_msgs::msg::PlanningWaypoint_<ContainerAllocator>>> & _arg)
  {
    this->path = _arg;
    return *this;
  }
  Type & set__path_as_lanes(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->path_as_lanes = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__PlanningInternalMissionPlanMsg
    std::shared_ptr<simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__PlanningInternalMissionPlanMsg
    std::shared_ptr<simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PlanningInternalMissionPlanMsg_ & other) const
  {
    if (this->path != other.path) {
      return false;
    }
    if (this->path_as_lanes != other.path_as_lanes) {
      return false;
    }
    return true;
  }
  bool operator!=(const PlanningInternalMissionPlanMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PlanningInternalMissionPlanMsg_

// alias to use template instance with default allocator
using PlanningInternalMissionPlanMsg =
  simple_av_msgs::msg::PlanningInternalMissionPlanMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PLANNING_INTERNAL_MISSION_PLAN_MSG__STRUCT_HPP_
