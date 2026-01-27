// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/TrafficSignalsArray.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__TrafficSignalsArray __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__TrafficSignalsArray __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TrafficSignalsArray_
{
  using Type = TrafficSignalsArray_<ContainerAllocator>;

  explicit TrafficSignalsArray_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit TrafficSignalsArray_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _v2i_traffic_signals_id_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _v2i_traffic_signals_id_type v2i_traffic_signals_id;
  using _v2i_traffic_signals_colors_type =
    std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>>;
  _v2i_traffic_signals_colors_type v2i_traffic_signals_colors;

  // setters for named parameter idiom
  Type & set__v2i_traffic_signals_id(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->v2i_traffic_signals_id = _arg;
    return *this;
  }
  Type & set__v2i_traffic_signals_colors(
    const std::vector<int32_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<int32_t>> & _arg)
  {
    this->v2i_traffic_signals_colors = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__TrafficSignalsArray
    std::shared_ptr<simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__TrafficSignalsArray
    std::shared_ptr<simple_av_msgs::msg::TrafficSignalsArray_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TrafficSignalsArray_ & other) const
  {
    if (this->v2i_traffic_signals_id != other.v2i_traffic_signals_id) {
      return false;
    }
    if (this->v2i_traffic_signals_colors != other.v2i_traffic_signals_colors) {
      return false;
    }
    return true;
  }
  bool operator!=(const TrafficSignalsArray_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TrafficSignalsArray_

// alias to use template instance with default allocator
using TrafficSignalsArray =
  simple_av_msgs::msg::TrafficSignalsArray_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__TRAFFIC_SIGNALS_ARRAY__STRUCT_HPP_
