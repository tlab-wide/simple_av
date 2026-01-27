// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_map_msgs:msg/LaneletMapCellMetaData.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_CELL_META_DATA__BUILDER_HPP_
#define AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_CELL_META_DATA__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_map_msgs/msg/detail/lanelet_map_cell_meta_data__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_map_msgs
{

namespace msg
{

namespace builder
{

class Init_LaneletMapCellMetaData_max_y
{
public:
  explicit Init_LaneletMapCellMetaData_max_y(::autoware_map_msgs::msg::LaneletMapCellMetaData & msg)
  : msg_(msg)
  {}
  ::autoware_map_msgs::msg::LaneletMapCellMetaData max_y(::autoware_map_msgs::msg::LaneletMapCellMetaData::_max_y_type arg)
  {
    msg_.max_y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_map_msgs::msg::LaneletMapCellMetaData msg_;
};

class Init_LaneletMapCellMetaData_min_y
{
public:
  explicit Init_LaneletMapCellMetaData_min_y(::autoware_map_msgs::msg::LaneletMapCellMetaData & msg)
  : msg_(msg)
  {}
  Init_LaneletMapCellMetaData_max_y min_y(::autoware_map_msgs::msg::LaneletMapCellMetaData::_min_y_type arg)
  {
    msg_.min_y = std::move(arg);
    return Init_LaneletMapCellMetaData_max_y(msg_);
  }

private:
  ::autoware_map_msgs::msg::LaneletMapCellMetaData msg_;
};

class Init_LaneletMapCellMetaData_max_x
{
public:
  explicit Init_LaneletMapCellMetaData_max_x(::autoware_map_msgs::msg::LaneletMapCellMetaData & msg)
  : msg_(msg)
  {}
  Init_LaneletMapCellMetaData_min_y max_x(::autoware_map_msgs::msg::LaneletMapCellMetaData::_max_x_type arg)
  {
    msg_.max_x = std::move(arg);
    return Init_LaneletMapCellMetaData_min_y(msg_);
  }

private:
  ::autoware_map_msgs::msg::LaneletMapCellMetaData msg_;
};

class Init_LaneletMapCellMetaData_min_x
{
public:
  explicit Init_LaneletMapCellMetaData_min_x(::autoware_map_msgs::msg::LaneletMapCellMetaData & msg)
  : msg_(msg)
  {}
  Init_LaneletMapCellMetaData_max_x min_x(::autoware_map_msgs::msg::LaneletMapCellMetaData::_min_x_type arg)
  {
    msg_.min_x = std::move(arg);
    return Init_LaneletMapCellMetaData_max_x(msg_);
  }

private:
  ::autoware_map_msgs::msg::LaneletMapCellMetaData msg_;
};

class Init_LaneletMapCellMetaData_cell_id
{
public:
  Init_LaneletMapCellMetaData_cell_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_LaneletMapCellMetaData_min_x cell_id(::autoware_map_msgs::msg::LaneletMapCellMetaData::_cell_id_type arg)
  {
    msg_.cell_id = std::move(arg);
    return Init_LaneletMapCellMetaData_min_x(msg_);
  }

private:
  ::autoware_map_msgs::msg::LaneletMapCellMetaData msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_map_msgs::msg::LaneletMapCellMetaData>()
{
  return autoware_map_msgs::msg::builder::Init_LaneletMapCellMetaData_cell_id();
}

}  // namespace autoware_map_msgs

#endif  // AUTOWARE_MAP_MSGS__MSG__DETAIL__LANELET_MAP_CELL_META_DATA__BUILDER_HPP_
