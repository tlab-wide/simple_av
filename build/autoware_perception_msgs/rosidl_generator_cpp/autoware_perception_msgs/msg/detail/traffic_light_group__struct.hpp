// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from autoware_perception_msgs:msg/TrafficLightGroup.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP__STRUCT_HPP_
#define AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'elements'
#include "autoware_perception_msgs/msg/detail/traffic_light_element__struct.hpp"
// Member 'predictions'
#include "autoware_perception_msgs/msg/detail/predicted_traffic_light_state__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__autoware_perception_msgs__msg__TrafficLightGroup __attribute__((deprecated))
#else
# define DEPRECATED__autoware_perception_msgs__msg__TrafficLightGroup __declspec(deprecated)
#endif

namespace autoware_perception_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct TrafficLightGroup_
{
  using Type = TrafficLightGroup_<ContainerAllocator>;

  explicit TrafficLightGroup_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->traffic_light_group_id = 0ll;
    }
  }

  explicit TrafficLightGroup_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->traffic_light_group_id = 0ll;
    }
  }

  // field types and members
  using _traffic_light_group_id_type =
    int64_t;
  _traffic_light_group_id_type traffic_light_group_id;
  using _elements_type =
    std::vector<autoware_perception_msgs::msg::TrafficLightElement_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_perception_msgs::msg::TrafficLightElement_<ContainerAllocator>>>;
  _elements_type elements;
  using _predictions_type =
    std::vector<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>>>;
  _predictions_type predictions;

  // setters for named parameter idiom
  Type & set__traffic_light_group_id(
    const int64_t & _arg)
  {
    this->traffic_light_group_id = _arg;
    return *this;
  }
  Type & set__elements(
    const std::vector<autoware_perception_msgs::msg::TrafficLightElement_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_perception_msgs::msg::TrafficLightElement_<ContainerAllocator>>> & _arg)
  {
    this->elements = _arg;
    return *this;
  }
  Type & set__predictions(
    const std::vector<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<autoware_perception_msgs::msg::PredictedTrafficLightState_<ContainerAllocator>>> & _arg)
  {
    this->predictions = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_perception_msgs__msg__TrafficLightGroup
    std::shared_ptr<autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_perception_msgs__msg__TrafficLightGroup
    std::shared_ptr<autoware_perception_msgs::msg::TrafficLightGroup_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const TrafficLightGroup_ & other) const
  {
    if (this->traffic_light_group_id != other.traffic_light_group_id) {
      return false;
    }
    if (this->elements != other.elements) {
      return false;
    }
    if (this->predictions != other.predictions) {
      return false;
    }
    return true;
  }
  bool operator!=(const TrafficLightGroup_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct TrafficLightGroup_

// alias to use template instance with default allocator
using TrafficLightGroup =
  autoware_perception_msgs::msg::TrafficLightGroup_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace autoware_perception_msgs

#endif  // AUTOWARE_PERCEPTION_MSGS__MSG__DETAIL__TRAFFIC_LIGHT_GROUP__STRUCT_HPP_
