// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/LocalizationMsg.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'closest_point'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'closest_lane_names'
#include "std_msgs/msg/detail/string__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__LocalizationMsg __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__LocalizationMsg __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct LocalizationMsg_
{
  using Type = LocalizationMsg_<ContainerAllocator>;

  explicit LocalizationMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : closest_point(_init),
    closest_lane_names(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->minimal_distance = 0.0;
    }
  }

  explicit LocalizationMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : closest_point(_alloc, _init),
    closest_lane_names(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->minimal_distance = 0.0;
    }
  }

  // field types and members
  using _closest_point_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _closest_point_type closest_point;
  using _closest_lane_names_type =
    std_msgs::msg::String_<ContainerAllocator>;
  _closest_lane_names_type closest_lane_names;
  using _minimal_distance_type =
    double;
  _minimal_distance_type minimal_distance;

  // setters for named parameter idiom
  Type & set__closest_point(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->closest_point = _arg;
    return *this;
  }
  Type & set__closest_lane_names(
    const std_msgs::msg::String_<ContainerAllocator> & _arg)
  {
    this->closest_lane_names = _arg;
    return *this;
  }
  Type & set__minimal_distance(
    const double & _arg)
  {
    this->minimal_distance = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__LocalizationMsg
    std::shared_ptr<simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__LocalizationMsg
    std::shared_ptr<simple_av_msgs::msg::LocalizationMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LocalizationMsg_ & other) const
  {
    if (this->closest_point != other.closest_point) {
      return false;
    }
    if (this->closest_lane_names != other.closest_lane_names) {
      return false;
    }
    if (this->minimal_distance != other.minimal_distance) {
      return false;
    }
    return true;
  }
  bool operator!=(const LocalizationMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LocalizationMsg_

// alias to use template instance with default allocator
using LocalizationMsg =
  simple_av_msgs::msg::LocalizationMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_MSG__STRUCT_HPP_
