// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from simple_av_msgs:msg/DetectedObject.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__STRUCT_HPP_
#define SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'position'
// Member 'bounding_box'
#include "geometry_msgs/msg/detail/point__struct.hpp"
// Member 'orientation'
#include "geometry_msgs/msg/detail/quaternion__struct.hpp"
// Member 'shape'
#include "geometry_msgs/msg/detail/vector3__struct.hpp"
// Member 'relative_direction'
#include "std_msgs/msg/detail/string__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__simple_av_msgs__msg__DetectedObject __attribute__((deprecated))
#else
# define DEPRECATED__simple_av_msgs__msg__DetectedObject __declspec(deprecated)
#endif

namespace simple_av_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct DetectedObject_
{
  using Type = DetectedObject_<ContainerAllocator>;

  explicit DetectedObject_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : position(_init),
    orientation(_init),
    shape(_init),
    relative_direction(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_from_rsu = false;
      this->label = 0l;
      this->velocity = 0.0;
      this->bounding_box.fill(geometry_msgs::msg::Point_<ContainerAllocator>{_init});
      this->distance = 0.0;
      this->nearest_object_side = 0l;
    }
  }

  explicit DetectedObject_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : position(_alloc, _init),
    orientation(_alloc, _init),
    shape(_alloc, _init),
    relative_direction(_alloc, _init),
    bounding_box(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->is_from_rsu = false;
      this->label = 0l;
      this->velocity = 0.0;
      this->bounding_box.fill(geometry_msgs::msg::Point_<ContainerAllocator>{_alloc, _init});
      this->distance = 0.0;
      this->nearest_object_side = 0l;
    }
  }

  // field types and members
  using _is_from_rsu_type =
    bool;
  _is_from_rsu_type is_from_rsu;
  using _label_type =
    int32_t;
  _label_type label;
  using _position_type =
    geometry_msgs::msg::Point_<ContainerAllocator>;
  _position_type position;
  using _velocity_type =
    double;
  _velocity_type velocity;
  using _orientation_type =
    geometry_msgs::msg::Quaternion_<ContainerAllocator>;
  _orientation_type orientation;
  using _shape_type =
    geometry_msgs::msg::Vector3_<ContainerAllocator>;
  _shape_type shape;
  using _relative_direction_type =
    std_msgs::msg::String_<ContainerAllocator>;
  _relative_direction_type relative_direction;
  using _bounding_box_type =
    std::array<geometry_msgs::msg::Point_<ContainerAllocator>, 4>;
  _bounding_box_type bounding_box;
  using _distance_type =
    double;
  _distance_type distance;
  using _nearest_object_side_type =
    int32_t;
  _nearest_object_side_type nearest_object_side;

  // setters for named parameter idiom
  Type & set__is_from_rsu(
    const bool & _arg)
  {
    this->is_from_rsu = _arg;
    return *this;
  }
  Type & set__label(
    const int32_t & _arg)
  {
    this->label = _arg;
    return *this;
  }
  Type & set__position(
    const geometry_msgs::msg::Point_<ContainerAllocator> & _arg)
  {
    this->position = _arg;
    return *this;
  }
  Type & set__velocity(
    const double & _arg)
  {
    this->velocity = _arg;
    return *this;
  }
  Type & set__orientation(
    const geometry_msgs::msg::Quaternion_<ContainerAllocator> & _arg)
  {
    this->orientation = _arg;
    return *this;
  }
  Type & set__shape(
    const geometry_msgs::msg::Vector3_<ContainerAllocator> & _arg)
  {
    this->shape = _arg;
    return *this;
  }
  Type & set__relative_direction(
    const std_msgs::msg::String_<ContainerAllocator> & _arg)
  {
    this->relative_direction = _arg;
    return *this;
  }
  Type & set__bounding_box(
    const std::array<geometry_msgs::msg::Point_<ContainerAllocator>, 4> & _arg)
  {
    this->bounding_box = _arg;
    return *this;
  }
  Type & set__distance(
    const double & _arg)
  {
    this->distance = _arg;
    return *this;
  }
  Type & set__nearest_object_side(
    const int32_t & _arg)
  {
    this->nearest_object_side = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    simple_av_msgs::msg::DetectedObject_<ContainerAllocator> *;
  using ConstRawPtr =
    const simple_av_msgs::msg::DetectedObject_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<simple_av_msgs::msg::DetectedObject_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<simple_av_msgs::msg::DetectedObject_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::DetectedObject_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::DetectedObject_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      simple_av_msgs::msg::DetectedObject_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<simple_av_msgs::msg::DetectedObject_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<simple_av_msgs::msg::DetectedObject_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<simple_av_msgs::msg::DetectedObject_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__simple_av_msgs__msg__DetectedObject
    std::shared_ptr<simple_av_msgs::msg::DetectedObject_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__simple_av_msgs__msg__DetectedObject
    std::shared_ptr<simple_av_msgs::msg::DetectedObject_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const DetectedObject_ & other) const
  {
    if (this->is_from_rsu != other.is_from_rsu) {
      return false;
    }
    if (this->label != other.label) {
      return false;
    }
    if (this->position != other.position) {
      return false;
    }
    if (this->velocity != other.velocity) {
      return false;
    }
    if (this->orientation != other.orientation) {
      return false;
    }
    if (this->shape != other.shape) {
      return false;
    }
    if (this->relative_direction != other.relative_direction) {
      return false;
    }
    if (this->bounding_box != other.bounding_box) {
      return false;
    }
    if (this->distance != other.distance) {
      return false;
    }
    if (this->nearest_object_side != other.nearest_object_side) {
      return false;
    }
    return true;
  }
  bool operator!=(const DetectedObject_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct DetectedObject_

// alias to use template instance with default allocator
using DetectedObject =
  simple_av_msgs::msg::DetectedObject_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace simple_av_msgs

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__DETECTED_OBJECT__STRUCT_HPP_
