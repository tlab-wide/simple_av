// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from autoware_internal_metric_msgs:msg/Metric.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__STRUCT_HPP_
#define AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__autoware_internal_metric_msgs__msg__Metric __attribute__((deprecated))
#else
# define DEPRECATED__autoware_internal_metric_msgs__msg__Metric __declspec(deprecated)
#endif

namespace autoware_internal_metric_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Metric_
{
  using Type = Metric_<ContainerAllocator>;

  explicit Metric_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
      this->unit = "";
      this->value = "";
    }
  }

  explicit Metric_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : name(_alloc),
    unit(_alloc),
    value(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->name = "";
      this->unit = "";
      this->value = "";
    }
  }

  // field types and members
  using _name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _name_type name;
  using _unit_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _unit_type unit;
  using _value_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _value_type value;

  // setters for named parameter idiom
  Type & set__name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->name = _arg;
    return *this;
  }
  Type & set__unit(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->unit = _arg;
    return *this;
  }
  Type & set__value(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->value = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_internal_metric_msgs__msg__Metric
    std::shared_ptr<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_internal_metric_msgs__msg__Metric
    std::shared_ptr<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Metric_ & other) const
  {
    if (this->name != other.name) {
      return false;
    }
    if (this->unit != other.unit) {
      return false;
    }
    if (this->value != other.value) {
      return false;
    }
    return true;
  }
  bool operator!=(const Metric_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Metric_

// alias to use template instance with default allocator
using Metric =
  autoware_internal_metric_msgs::msg::Metric_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace autoware_internal_metric_msgs

#endif  // AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC__STRUCT_HPP_
