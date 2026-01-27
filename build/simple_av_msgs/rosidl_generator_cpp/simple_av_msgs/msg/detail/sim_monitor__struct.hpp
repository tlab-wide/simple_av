// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/SimMonitor.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__SimMonitor __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__SimMonitor __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SimMonitor_
{
  using Type = SimMonitor_<ContainerAllocator>;

  explicit SimMonitor_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->system_time = 0.0;
      this->sim_time = 0.0;
      this->sim_clock_rate = 0.0;
    }
  }

  explicit SimMonitor_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->system_time = 0.0;
      this->sim_time = 0.0;
      this->sim_clock_rate = 0.0;
    }
  }

  // field types and members
  using _system_time_type =
    double;
  _system_time_type system_time;
  using _sim_time_type =
    double;
  _sim_time_type sim_time;
  using _sim_clock_rate_type =
    double;
  _sim_clock_rate_type sim_clock_rate;

  // setters for named parameter idiom
  Type & set__system_time(
    const double & _arg)
  {
    this->system_time = _arg;
    return *this;
  }
  Type & set__sim_time(
    const double & _arg)
  {
    this->sim_time = _arg;
    return *this;
  }
  Type & set__sim_clock_rate(
    const double & _arg)
  {
    this->sim_clock_rate = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::SimMonitor_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::SimMonitor_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::SimMonitor_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::SimMonitor_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::SimMonitor_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::SimMonitor_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::SimMonitor_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::SimMonitor_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::SimMonitor_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::SimMonitor_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__SimMonitor
    std::shared_ptr<simple_av_msgs::msg::SimMonitor_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__SimMonitor
    std::shared_ptr<simple_av_msgs::msg::SimMonitor_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SimMonitor_ & other) const
  {
    if (this->system_time != other.system_time) {
      return false;
    }
    if (this->sim_time != other.sim_time) {
      return false;
    }
    if (this->sim_clock_rate != other.sim_clock_rate) {
      return false;
    }
    return true;
  }
  bool operator!=(const SimMonitor_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SimMonitor_

// alias to use template instance with default allocator
using SimMonitor =
  simple_av_msgs::msg::SimMonitor_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__STRUCT_HPP_
