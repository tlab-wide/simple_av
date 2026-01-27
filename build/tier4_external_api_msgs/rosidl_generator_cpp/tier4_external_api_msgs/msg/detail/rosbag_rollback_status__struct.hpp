// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from tier4_external_api_msgs:msg/RosbagRollbackStatus.idl
// generated code does not contain a copyright notice

#ifndef TIER4_EXTERNAL_API_MSGS__MSG__DETAIL__ROSBAG_ROLLBACK_STATUS__STRUCT_HPP_
#define TIER4_EXTERNAL_API_MSGS__MSG__DETAIL__ROSBAG_ROLLBACK_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__tier4_external_api_msgs__msg__RosbagRollbackStatus __attribute__((deprecated))
#else
# define DEPRECATED__tier4_external_api_msgs__msg__RosbagRollbackStatus __declspec(deprecated)
#endif

namespace tier4_external_api_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct RosbagRollbackStatus_
{
  using Type = RosbagRollbackStatus_<ContainerAllocator>;

  explicit RosbagRollbackStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
      this->message = "";
      this->progress = 0.0;
      this->bytes_to_copy = 0ull;
      this->bytes_copied = 0ull;
      this->elapsed_time = 0.0;
      this->estimated_time = 0.0;
      this->remaining_time = 0.0;
    }
  }

  explicit RosbagRollbackStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->status = 0;
      this->message = "";
      this->progress = 0.0;
      this->bytes_to_copy = 0ull;
      this->bytes_copied = 0ull;
      this->elapsed_time = 0.0;
      this->estimated_time = 0.0;
      this->remaining_time = 0.0;
    }
  }

  // field types and members
  using _status_type =
    uint8_t;
  _status_type status;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _progress_type =
    double;
  _progress_type progress;
  using _bytes_to_copy_type =
    uint64_t;
  _bytes_to_copy_type bytes_to_copy;
  using _bytes_copied_type =
    uint64_t;
  _bytes_copied_type bytes_copied;
  using _elapsed_time_type =
    double;
  _elapsed_time_type elapsed_time;
  using _estimated_time_type =
    double;
  _estimated_time_type estimated_time;
  using _remaining_time_type =
    double;
  _remaining_time_type remaining_time;

  // setters for named parameter idiom
  Type & set__status(
    const uint8_t & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }
  Type & set__progress(
    const double & _arg)
  {
    this->progress = _arg;
    return *this;
  }
  Type & set__bytes_to_copy(
    const uint64_t & _arg)
  {
    this->bytes_to_copy = _arg;
    return *this;
  }
  Type & set__bytes_copied(
    const uint64_t & _arg)
  {
    this->bytes_copied = _arg;
    return *this;
  }
  Type & set__elapsed_time(
    const double & _arg)
  {
    this->elapsed_time = _arg;
    return *this;
  }
  Type & set__estimated_time(
    const double & _arg)
  {
    this->estimated_time = _arg;
    return *this;
  }
  Type & set__remaining_time(
    const double & _arg)
  {
    this->remaining_time = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint8_t READY =
    0u;
  static constexpr uint8_t IN_PROGRESS =
    1u;
  static constexpr uint8_t STOP_IN_PROGRESS =
    2u;
  static constexpr uint8_t COMPLETED =
    3u;
  static constexpr uint8_t STOP_COMPLETED =
    4u;
  // guard against 'ERROR' being predefined by MSVC by temporarily undefining it
#if defined(_WIN32)
#  if defined(ERROR)
#    pragma push_macro("ERROR")
#    undef ERROR
#  endif
#endif
  static constexpr uint8_t ERROR =
    5u;
#if defined(_WIN32)
#  pragma warning(suppress : 4602)
#  pragma pop_macro("ERROR")
#endif

  // pointer types
  using RawPtr =
    tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__tier4_external_api_msgs__msg__RosbagRollbackStatus
    std::shared_ptr<tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__tier4_external_api_msgs__msg__RosbagRollbackStatus
    std::shared_ptr<tier4_external_api_msgs::msg::RosbagRollbackStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const RosbagRollbackStatus_ & other) const
  {
    if (this->status != other.status) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->progress != other.progress) {
      return false;
    }
    if (this->bytes_to_copy != other.bytes_to_copy) {
      return false;
    }
    if (this->bytes_copied != other.bytes_copied) {
      return false;
    }
    if (this->elapsed_time != other.elapsed_time) {
      return false;
    }
    if (this->estimated_time != other.estimated_time) {
      return false;
    }
    if (this->remaining_time != other.remaining_time) {
      return false;
    }
    return true;
  }
  bool operator!=(const RosbagRollbackStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct RosbagRollbackStatus_

// alias to use template instance with default allocator
using RosbagRollbackStatus =
  tier4_external_api_msgs::msg::RosbagRollbackStatus_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RosbagRollbackStatus_<ContainerAllocator>::READY;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RosbagRollbackStatus_<ContainerAllocator>::IN_PROGRESS;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RosbagRollbackStatus_<ContainerAllocator>::STOP_IN_PROGRESS;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RosbagRollbackStatus_<ContainerAllocator>::COMPLETED;
#endif  // __cplusplus < 201703L
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RosbagRollbackStatus_<ContainerAllocator>::STOP_COMPLETED;
#endif  // __cplusplus < 201703L
// guard against 'ERROR' being predefined by MSVC by temporarily undefining it
#if defined(_WIN32)
#  if defined(ERROR)
#    pragma push_macro("ERROR")
#    undef ERROR
#  endif
#endif
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint8_t RosbagRollbackStatus_<ContainerAllocator>::ERROR;
#endif  // __cplusplus < 201703L
#if defined(_WIN32)
#  pragma warning(suppress : 4602)
#  pragma pop_macro("ERROR")
#endif

}  // namespace msg

}  // namespace tier4_external_api_msgs

#endif  // TIER4_EXTERNAL_API_MSGS__MSG__DETAIL__ROSBAG_ROLLBACK_STATUS__STRUCT_HPP_
