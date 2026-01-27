// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from autoware_map_msgs:msg/LaneletMapCellMetaData.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_CELL_META_DATA__STRUCT_HPP_
#define AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_CELL_META_DATA__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__autoware_map_msgs__msg__LaneletMapCellMetaData __attribute__((deprecated))
#else
# define DEPRECATED__autoware_map_msgs__msg__LaneletMapCellMetaData __declspec(deprecated)
#endif

namespace autoware_map_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct LaneletMapCellMetaData_
{
  using Type = LaneletMapCellMetaData_<ContainerAllocator>;

  explicit LaneletMapCellMetaData_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->cell_id = "";
      this->min_x = 0.0;
      this->max_x = 0.0;
      this->min_y = 0.0;
      this->max_y = 0.0;
    }
  }

  explicit LaneletMapCellMetaData_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : cell_id(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->cell_id = "";
      this->min_x = 0.0;
      this->max_x = 0.0;
      this->min_y = 0.0;
      this->max_y = 0.0;
    }
  }

  // field types and members
  using _cell_id_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _cell_id_type cell_id;
  using _min_x_type =
    double;
  _min_x_type min_x;
  using _max_x_type =
    double;
  _max_x_type max_x;
  using _min_y_type =
    double;
  _min_y_type min_y;
  using _max_y_type =
    double;
  _max_y_type max_y;

  // setters for named parameter idiom
  Type & set__cell_id(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->cell_id = _arg;
    return *this;
  }
  Type & set__min_x(
    const double & _arg)
  {
    this->min_x = _arg;
    return *this;
  }
  Type & set__max_x(
    const double & _arg)
  {
    this->max_x = _arg;
    return *this;
  }
  Type & set__min_y(
    const double & _arg)
  {
    this->min_y = _arg;
    return *this;
  }
  Type & set__max_y(
    const double & _arg)
  {
    this->max_y = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_map_msgs__msg__LaneletMapCellMetaData
    std::shared_ptr<autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_map_msgs__msg__LaneletMapCellMetaData
    std::shared_ptr<autoware_map_msgs::msg::LaneletMapCellMetaData_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LaneletMapCellMetaData_ & other) const
  {
    if (this->cell_id != other.cell_id) {
      return false;
    }
    if (this->min_x != other.min_x) {
      return false;
    }
    if (this->max_x != other.max_x) {
      return false;
    }
    if (this->min_y != other.min_y) {
      return false;
    }
    if (this->max_y != other.max_y) {
      return false;
    }
    return true;
  }
  bool operator!=(const LaneletMapCellMetaData_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LaneletMapCellMetaData_

// alias to use template instance with default allocator
using LaneletMapCellMetaData =
  autoware_map_msgs::msg::LaneletMapCellMetaData_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace autoware_map_msgs

#endif  // AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_CELL_META_DATA__STRUCT_HPP_
