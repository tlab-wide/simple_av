// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:srv/TriggerMissionPlan.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__STRUCT_HPP_
#define SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__srv__TriggerMissionPlan_Request __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__srv__TriggerMissionPlan_Request __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct TriggerMissionPlan_Request_
{
  using Type = TriggerMissionPlan_Request_<ContainerAllocator>;

  explicit TriggerMissionPlan_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit TriggerMissionPlan_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__srv__TriggerMissionPlan_Request
    std::shared_ptr<simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__srv__TriggerMissionPlan_Request
    std::shared_ptr<simple_av_msgs::srv::TriggerMissionPlan_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TriggerMissionPlan_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const TriggerMissionPlan_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TriggerMissionPlan_Request_

// alias to use template instance with default allocator
using TriggerMissionPlan_Request =
  simple_av_msgs::srv::TriggerMissionPlan_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace simple_av_msgs


#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__srv__TriggerMissionPlan_Response __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__srv__TriggerMissionPlan_Response __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct TriggerMissionPlan_Response_
{
  using Type = TriggerMissionPlan_Response_<ContainerAllocator>;

  explicit TriggerMissionPlan_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  explicit TriggerMissionPlan_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__srv__TriggerMissionPlan_Response
    std::shared_ptr<simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__srv__TriggerMissionPlan_Response
    std::shared_ptr<simple_av_msgs::srv::TriggerMissionPlan_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TriggerMissionPlan_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const TriggerMissionPlan_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TriggerMissionPlan_Response_

// alias to use template instance with default allocator
using TriggerMissionPlan_Response =
  simple_av_msgs::srv::TriggerMissionPlan_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace simple_av_msgs

namespace simple_av_msgs
{

namespace srv
{

struct TriggerMissionPlan
{
  using Request = simple_av_msgs::srv::TriggerMissionPlan_Request;
  using Response = simple_av_msgs::srv::TriggerMissionPlan_Response;
};

}  // namespace srv

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__SRV__DETAIL__TRIGGER_MISSION_PLAN__STRUCT_HPP_
