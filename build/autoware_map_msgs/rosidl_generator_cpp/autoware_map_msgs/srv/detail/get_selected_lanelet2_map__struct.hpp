// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from autoware_map_msgs:srv/GetSelectedLanelet2Map.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_MAP_MSGS__SRV__DETAIL__GET_SELECTED_LANELET2_MAP__STRUCT_HPP_
#define AUTOWARE_MAP_MSGS__SRV__DETAIL__GET_SELECTED_LANELET2_MAP__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__autoware_map_msgs__srv__GetSelectedLanelet2Map_Request __attribute__((deprecated))
#else
# define DEPRECATED__autoware_map_msgs__srv__GetSelectedLanelet2Map_Request __declspec(deprecated)
#endif

namespace autoware_map_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetSelectedLanelet2Map_Request_
{
  using Type = GetSelectedLanelet2Map_Request_<ContainerAllocator>;

  explicit GetSelectedLanelet2Map_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit GetSelectedLanelet2Map_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _cell_ids_type =
    std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>>;
  _cell_ids_type cell_ids;

  // setters for named parameter idiom
  Type & set__cell_ids(
    const std::vector<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>>> & _arg)
  {
    this->cell_ids = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_map_msgs__srv__GetSelectedLanelet2Map_Request
    std::shared_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_map_msgs__srv__GetSelectedLanelet2Map_Request
    std::shared_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetSelectedLanelet2Map_Request_ & other) const
  {
    if (this->cell_ids != other.cell_ids) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetSelectedLanelet2Map_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetSelectedLanelet2Map_Request_

// alias to use template instance with default allocator
using GetSelectedLanelet2Map_Request =
  autoware_map_msgs::srv::GetSelectedLanelet2Map_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace autoware_map_msgs


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"
// Member 'lanelet2_cells'
#include "autoware_map_msgs/msg/detail/lanelet_map_bin__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__autoware_map_msgs__srv__GetSelectedLanelet2Map_Response __attribute__((deprecated))
#else
# define DEPRECATED__autoware_map_msgs__srv__GetSelectedLanelet2Map_Response __declspec(deprecated)
#endif

namespace autoware_map_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetSelectedLanelet2Map_Response_
{
  using Type = GetSelectedLanelet2Map_Response_<ContainerAllocator>;

  explicit GetSelectedLanelet2Map_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init),
    lanelet2_cells(_init)
  {
    (void)_init;
  }

  explicit GetSelectedLanelet2Map_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    lanelet2_cells(_alloc, _init)
  {
    (void)_init;
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _lanelet2_cells_type =
    autoware_map_msgs::msg::LaneletMapBin_<ContainerAllocator>;
  _lanelet2_cells_type lanelet2_cells;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__lanelet2_cells(
    const autoware_map_msgs::msg::LaneletMapBin_<ContainerAllocator> & _arg)
  {
    this->lanelet2_cells = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__autoware_map_msgs__srv__GetSelectedLanelet2Map_Response
    std::shared_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__autoware_map_msgs__srv__GetSelectedLanelet2Map_Response
    std::shared_ptr<autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetSelectedLanelet2Map_Response_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->lanelet2_cells != other.lanelet2_cells) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetSelectedLanelet2Map_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetSelectedLanelet2Map_Response_

// alias to use template instance with default allocator
using GetSelectedLanelet2Map_Response =
  autoware_map_msgs::srv::GetSelectedLanelet2Map_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace autoware_map_msgs

namespace autoware_map_msgs
{

namespace srv
{

struct GetSelectedLanelet2Map
{
  using Request = autoware_map_msgs::srv::GetSelectedLanelet2Map_Request;
  using Response = autoware_map_msgs::srv::GetSelectedLanelet2Map_Response;
};

}  // namespace srv

}  // namespace autoware_map_msgs

#endif  // AUTOWARE_MAP_MSGS__SRV__DETAIL__GET_SELECTED_LANELET2_MAP__STRUCT_HPP_
