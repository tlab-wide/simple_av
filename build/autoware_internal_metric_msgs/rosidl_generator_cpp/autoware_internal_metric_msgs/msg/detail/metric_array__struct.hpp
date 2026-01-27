// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from autoware_internal_metric_msgs:msg/MetricArray.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__STRUCT_HPP_
#define AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"
// Member 'metric_array'
#include "autoware_internal_metric_msgs/msg/detail/metric__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__autoware_internal_metric_msgs__msg__MetricArray __attribute__((deprecated))
#else
# define DEPRECATED__autoware_internal_metric_msgs__msg__MetricArray __declspec(deprecated)
#endif

namespace autoware_internal_metric_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MetricArray_
{
  using Type = MetricArray_<ContainerAllocator>;

  explicit MetricArray_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_init)
  {
    (void)_init;
  }

  explicit MetricArray_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : stamp(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _stamp_type stamp;
  using _metric_array_type =
    std::vector<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>>>;
  _metric_array_type metric_array;

  // setters for named parameter idiom
  Type & set__stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->stamp = _arg;
    return *this;
  }
  Type & set__metric_array(
    const std::vector<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_internal_metric_msgs::msg::Metric_<ContainerAllocator>>> & _arg)
  {
    this->metric_array = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_internal_metric_msgs__msg__MetricArray
    std::shared_ptr<autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_internal_metric_msgs__msg__MetricArray
    std::shared_ptr<autoware_internal_metric_msgs::msg::MetricArray_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MetricArray_ & other) const
  {
    if (this->stamp != other.stamp) {
      return false;
    }
    if (this->metric_array != other.metric_array) {
      return false;
    }
    return true;
  }
  bool operator!=(const MetricArray_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MetricArray_

// alias to use template instance with default allocator
using MetricArray =
  autoware_internal_metric_msgs::msg::MetricArray_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace autoware_internal_metric_msgs

#endif  // AUTOWARE_INTERNAL_METRIC_MSGS__MSG__DETAIL__METRIC_ARRAY__STRUCT_HPP_
