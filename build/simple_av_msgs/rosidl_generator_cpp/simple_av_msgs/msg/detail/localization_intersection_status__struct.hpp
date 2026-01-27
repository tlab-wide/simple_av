// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/LocalizationIntersectionStatus.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__LocalizationIntersectionStatus __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__LocalizationIntersectionStatus __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct LocalizationIntersectionStatus_
{
  using Type = LocalizationIntersectionStatus_<ContainerAllocator>;

  explicit LocalizationIntersectionStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->intersection_name = "";
      this->status = "";
      this->distance_to_intersection = 0.0f;
    }
  }

  explicit LocalizationIntersectionStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : intersection_name(_alloc),
    status(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->intersection_name = "";
      this->status = "";
      this->distance_to_intersection = 0.0f;
    }
  }

  // field types and members
  using _intersection_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _intersection_name_type intersection_name;
  using _status_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _status_type status;
  using _distance_to_intersection_type =
    float;
  _distance_to_intersection_type distance_to_intersection;

  // setters for named parameter idiom
  Type & set__intersection_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->intersection_name = _arg;
    return *this;
  }
  Type & set__status(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__distance_to_intersection(
    const float & _arg)
  {
    this->distance_to_intersection = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__LocalizationIntersectionStatus
    std::shared_ptr<simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__LocalizationIntersectionStatus
    std::shared_ptr<simple_av_msgs::msg::LocalizationIntersectionStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LocalizationIntersectionStatus_ & other) const
  {
    if (this->intersection_name != other.intersection_name) {
      return false;
    }
    if (this->status != other.status) {
      return false;
    }
    if (this->distance_to_intersection != other.distance_to_intersection) {
      return false;
    }
    return true;
  }
  bool operator!=(const LocalizationIntersectionStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LocalizationIntersectionStatus_

// alias to use template instance with default allocator
using LocalizationIntersectionStatus =
  simple_av_msgs::msg::LocalizationIntersectionStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__LOCALIZATION_INTERSECTION_STATUS__STRUCT_HPP_
