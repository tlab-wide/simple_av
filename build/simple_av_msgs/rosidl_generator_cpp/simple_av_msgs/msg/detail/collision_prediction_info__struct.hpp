// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/CollisionPredictionInfo.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'object_position'
#include "geometry_msgs/msg/detail/point__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__CollisionPredictionInfo __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__CollisionPredictionInfo __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CollisionPredictionInfo_
{
  using Type = CollisionPredictionInfo_<ContainerAllocator>;

  explicit CollisionPredictionInfo_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : object_position(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->time_to_collision = 0.0;
      this->object_label = 0l;
      this->object_velocity = 0.0;
      this->collision_detected = false;
    }
  }

  explicit CollisionPredictionInfo_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : object_position(_alloc, _init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->time_to_collision = 0.0;
      this->object_label = 0l;
      this->object_velocity = 0.0;
      this->collision_detected = false;
    }
  }

  // field types and members
  using _object_position_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _object_position_type object_position;
  using _time_to_collision_type =
    double;
  _time_to_collision_type time_to_collision;
  using _object_label_type =
    int32_t;
  _object_label_type object_label;
  using _object_velocity_type =
    double;
  _object_velocity_type object_velocity;
  using _collision_detected_type =
    bool;
  _collision_detected_type collision_detected;

  // setters for named parameter idiom
  Type & set__object_position(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->object_position = _arg;
    return *this;
  }
  Type & set__time_to_collision(
    const double & _arg)
  {
    this->time_to_collision = _arg;
    return *this;
  }
  Type & set__object_label(
    const int32_t & _arg)
  {
    this->object_label = _arg;
    return *this;
  }
  Type & set__object_velocity(
    const double & _arg)
  {
    this->object_velocity = _arg;
    return *this;
  }
  Type & set__collision_detected(
    const bool & _arg)
  {
    this->collision_detected = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__CollisionPredictionInfo
    std::shared_ptr<simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__CollisionPredictionInfo
    std::shared_ptr<simple_av_msgs::msg::CollisionPredictionInfo_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CollisionPredictionInfo_ & other) const
  {
    if (this->object_position != other.object_position) {
      return false;
    }
    if (this->time_to_collision != other.time_to_collision) {
      return false;
    }
    if (this->object_label != other.object_label) {
      return false;
    }
    if (this->object_velocity != other.object_velocity) {
      return false;
    }
    if (this->collision_detected != other.collision_detected) {
      return false;
    }
    return true;
  }
  bool operator!=(const CollisionPredictionInfo_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CollisionPredictionInfo_

// alias to use template instance with default allocator
using CollisionPredictionInfo =
  simple_av_msgs::msg::CollisionPredictionInfo_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__COLLISION_PREDICTION_INFO__STRUCT_HPP_
