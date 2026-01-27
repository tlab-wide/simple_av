// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from autoware_perception_msgs:msg/PredictedTrafficLightState.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__STRUCT_HPP_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'predicted_stamp'
#include "builtin_interfaces/msg/detail/time__struct.hpp"
// Member 'simultaneous_elements'
#include "autoware_perception_msgs/msg/detail/traffic_light_element__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__autoware_perception_msgs__msg__PredictedTrafficLightState __attribute__((deprecated))
#else
# define DEPRECATED__autoware_perception_msgs__msg__PredictedTrafficLightState __declspec(deprecated)
#endif

namespace autoware_perception_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PredictedTrafficLightState_
{
  using Type = PredictedTrafficLightState_<ContainerAllocator>;

  explicit PredictedTrafficLightState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : predicted_stamp(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reliability = 0.0f;
      this->information_source = "";
    }
  }

  explicit PredictedTrafficLightState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : predicted_stamp(_alloc, _init),
    information_source(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->reliability = 0.0f;
      this->information_source = "";
    }
  }

  // field types and members
  using _predicted_stamp_type =
    builtin_interfaces::msg::Time_<ContainerAllocator>;
  _predicted_stamp_type predicted_stamp;
  using _simultaneous_elements_type =
    std::vector<autoware_perception_msgs::msg::TrafficLightElement_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_perception_msgs::msg::TrafficLightElement_<ContainerAllocator>>>;
  _simultaneous_elements_type simultaneous_elements;
  using _reliability_type =
    float;
  _reliability_type reliability;
  using _information_source_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _information_source_type information_source;

  // setters for named parameter idiom
  Type & set__predicted_stamp(
    const builtin_interfaces::msg::Time_<ContainerAllocator> & _arg)
  {
    this->predicted_stamp = _arg;
    return *this;
  }
  Type & set__simultaneous_elements(
    const std::vector<autoware_perception_msgs::msg::TrafficLightElement_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_perception_msgs::msg::TrafficLightElement_<ContainerAllocator>>> & _arg)
  {
    this->simultaneous_elements = _arg;
    return *this;
  }
  Type & set__reliability(
    const float & _arg)
  {
    this->reliability = _arg;
    return *this;
  }
  Type & set__information_source(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->information_source = _arg;
    return *this;
  }

  // constant declarations
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INFORMATION_SOURCE_V2N;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INFORMATION_SOURCE_V2I;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INFORMATION_SOURCE_V2V;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INFORMATION_SOURCE_LOCAL_PERCEPTION;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INFORMATION_SOURCE_MANUAL_OVERRIDE;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INFORMATION_SOURCE_SIMULATION;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INFORMATION_SOURCE_INTERNAL_ESTIMATION;

  // pointer types
  using RawPtr =
    autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_perception_msgs__msg__PredictedTrafficLightState
    std::shared_ptr<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_perception_msgs__msg__PredictedTrafficLightState
    std::shared_ptr<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PredictedTrafficLightState_ & other) const
  {
    if (this->predicted_stamp != other.predicted_stamp) {
      return false;
    }
    if (this->simultaneous_elements != other.simultaneous_elements) {
      return false;
    }
    if (this->reliability != other.reliability) {
      return false;
    }
    if (this->information_source != other.information_source) {
      return false;
    }
    return true;
  }
  bool operator!=(const PredictedTrafficLightState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PredictedTrafficLightState_

// alias to use template instance with default allocator
using PredictedTrafficLightState =
  autoware_perception_msgs::msg::PredictedTrafficLightState_<std::allocator<void>>;

// constant definitions
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
PredictedTrafficLightState_<ContainerAllocator>::INFORMATION_SOURCE_V2N = "V2N";
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
PredictedTrafficLightState_<ContainerAllocator>::INFORMATION_SOURCE_V2I = "V2I";
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
PredictedTrafficLightState_<ContainerAllocator>::INFORMATION_SOURCE_V2V = "V2V";
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
PredictedTrafficLightState_<ContainerAllocator>::INFORMATION_SOURCE_LOCAL_PERCEPTION = "LOCAL_PERCEPTION";
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
PredictedTrafficLightState_<ContainerAllocator>::INFORMATION_SOURCE_MANUAL_OVERRIDE = "MANUAL_OVERRIDE";
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
PredictedTrafficLightState_<ContainerAllocator>::INFORMATION_SOURCE_SIMULATION = "SIMULATION";
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
PredictedTrafficLightState_<ContainerAllocator>::INFORMATION_SOURCE_INTERNAL_ESTIMATION = "INTERNAL_ESTIMATION";

}  // namespace msg

}  // namespace autoware_perception_msgs

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__PREDICTED_TRAFFIC_LIGHT_STATE__STRUCT_HPP_
