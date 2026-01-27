// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeTree.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__STRUCT_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'nodes'
#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__autoware_internal_debug_msgs__msg__ProcessingTimeTree __attribute__((deprecated))
#else
# define DEPRECATED__autoware_internal_debug_msgs__msg__ProcessingTimeTree __declspec(deprecated)
#endif

namespace autoware_internal_debug_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct ProcessingTimeTree_
{
  using Type = ProcessingTimeTree_<ContainerAllocator>;

  explicit ProcessingTimeTree_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit ProcessingTimeTree_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _nodes_type =
    std::vector<autoware_internal_debug_msgs::msg::ProcessingTimeNode_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_internal_debug_msgs::msg::ProcessingTimeNode_<ContainerAllocator>>>;
  _nodes_type nodes;

  // setters for named parameter idiom
  Type & set__nodes(
    const std::vector<autoware_internal_debug_msgs::msg::ProcessingTimeNode_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_internal_debug_msgs::msg::ProcessingTimeNode_<ContainerAllocator>>> & _arg)
  {
    this->nodes = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_internal_debug_msgs__msg__ProcessingTimeTree
    std::shared_ptr<autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_internal_debug_msgs__msg__ProcessingTimeTree
    std::shared_ptr<autoware_internal_debug_msgs::msg::ProcessingTimeTree_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const ProcessingTimeTree_ & other) const
  {
    if (this->nodes != other.nodes) {
      return false;
    }
    return true;
  }
  bool operator!=(const ProcessingTimeTree_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct ProcessingTimeTree_

// alias to use template instance with default allocator
using ProcessingTimeTree =
  autoware_internal_debug_msgs::msg::ProcessingTimeTree_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace autoware_internal_debug_msgs

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__MSG__DETAIL__PROCESSING_TIME_TREE__STRUCT_HPP_
