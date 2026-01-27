// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from autoware_internal_debug_msgs:srv/String.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__STRUCT_HPP_
#define AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__autoware_internal_debug_msgs__srv__String_Request __attribute__((deprecated))
#else
# define DEPRECATED__autoware_internal_debug_msgs__srv__String_Request __declspec(deprecated)
#endif

namespace autoware_internal_debug_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct String_Request_
{
  using Type = String_Request_<ContainerAllocator>;

  explicit String_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data = "";
    }
  }

  explicit String_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : data(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->data = "";
    }
  }

  // field types and members
  using _data_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _data_type data;

  // setters for named parameter idiom
  Type & set__data(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->data = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_internal_debug_msgs__srv__String_Request
    std::shared_ptr<autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_internal_debug_msgs__srv__String_Request
    std::shared_ptr<autoware_internal_debug_msgs::srv::String_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const String_Request_ & other) const
  {
    if (this->data != other.data) {
      return false;
    }
    return true;
  }
  bool operator!=(const String_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct String_Request_

// alias to use template instance with default allocator
using String_Request =
  autoware_internal_debug_msgs::srv::String_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace autoware_internal_debug_msgs


#ifndef _WIN32
# define DEPRECATED__autoware_internal_debug_msgs__srv__String_Response __attribute__((deprecated))
#else
# define DEPRECATED__autoware_internal_debug_msgs__srv__String_Response __declspec(deprecated)
#endif

namespace autoware_internal_debug_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct String_Response_
{
  using Type = String_Response_<ContainerAllocator>;

  explicit String_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  explicit String_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_internal_debug_msgs__srv__String_Response
    std::shared_ptr<autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_internal_debug_msgs__srv__String_Response
    std::shared_ptr<autoware_internal_debug_msgs::srv::String_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const String_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    return true;
  }
  bool operator!=(const String_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct String_Response_

// alias to use template instance with default allocator
using String_Response =
  autoware_internal_debug_msgs::srv::String_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace autoware_internal_debug_msgs

namespace autoware_internal_debug_msgs
{

namespace srv
{

struct String
{
  using Request = autoware_internal_debug_msgs::srv::String_Request;
  using Response = autoware_internal_debug_msgs::srv::String_Response;
};

}  // namespace srv

}  // namespace autoware_internal_debug_msgs

#endif  // AUTOWARE_INTERNAL_DEBUG_MSGS__SRV__DETAIL__STRING__STRUCT_HPP_
