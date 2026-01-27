// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/Portal.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__Portal __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__Portal __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Portal_
{
  using Type = Portal_<ContainerAllocator>;

  explicit Portal_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reset = false;
      this->round_number = 0l;
      this->finished = false;
    }
  }

  explicit Portal_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reset = false;
      this->round_number = 0l;
      this->finished = false;
    }
  }

  // field types and members
  using _reset_type =
    bool;
  _reset_type reset;
  using _round_number_type =
    int32_t;
  _round_number_type round_number;
  using _finished_type =
    bool;
  _finished_type finished;

  // setters for named parameter idiom
  Type & set__reset(
    const bool & _arg)
  {
    this->reset = _arg;
    return *this;
  }
  Type & set__round_number(
    const int32_t & _arg)
  {
    this->round_number = _arg;
    return *this;
  }
  Type & set__finished(
    const bool & _arg)
  {
    this->finished = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::Portal_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::Portal_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::Portal_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::Portal_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::Portal_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::Portal_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::Portal_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::Portal_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::Portal_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::Portal_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__Portal
    std::shared_ptr<simple_av_msgs::msg::Portal_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__Portal
    std::shared_ptr<simple_av_msgs::msg::Portal_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Portal_ & other) const
  {
    if (this->reset != other.reset) {
      return false;
    }
    if (this->round_number != other.round_number) {
      return false;
    }
    if (this->finished != other.finished) {
      return false;
    }
    return true;
  }
  bool operator!=(const Portal_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Portal_

// alias to use template instance with default allocator
using Portal =
  simple_av_msgs::msg::Portal_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__PORTAL__STRUCT_HPP_
