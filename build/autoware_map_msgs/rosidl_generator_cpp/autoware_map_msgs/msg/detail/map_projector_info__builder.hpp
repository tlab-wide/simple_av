// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from autoware_map_msgs:msg/MapProjectorInfo.idl
// generated code does not contain a copyright notice

#ifndef AUTOWARE_MAP_MSGS__MSG__DETAIL__MAP_PROJECTOR_INFO__BUILDER_HPP_
#define AUTOWARE_MAP_MSGS__MSG__DETAIL__MAP_PROJECTOR_INFO__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "autoware_map_msgs/msg/detail/map_projector_info__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace autoware_map_msgs
{

namespace msg
{

namespace builder
{

class Init_MapProjectorInfo_scale_factor
{
public:
  explicit Init_MapProjectorInfo_scale_factor(::autoware_map_msgs::msg::MapProjectorInfo & msg)
  : msg_(msg)
  {}
  ::autoware_map_msgs::msg::MapProjectorInfo scale_factor(::autoware_map_msgs::msg::MapProjectorInfo::_scale_factor_type arg)
  {
    msg_.scale_factor = std::move(arg);
    return std::move(msg_);
  }

private:
  ::autoware_map_msgs::msg::MapProjectorInfo msg_;
};

class Init_MapProjectorInfo_map_origin
{
public:
  explicit Init_MapProjectorInfo_map_origin(::autoware_map_msgs::msg::MapProjectorInfo & msg)
  : msg_(msg)
  {}
  Init_MapProjectorInfo_scale_factor map_origin(::autoware_map_msgs::msg::MapProjectorInfo::_map_origin_type arg)
  {
    msg_.map_origin = std::move(arg);
    return Init_MapProjectorInfo_scale_factor(msg_);
  }

private:
  ::autoware_map_msgs::msg::MapProjectorInfo msg_;
};

class Init_MapProjectorInfo_mgrs_grid
{
public:
  explicit Init_MapProjectorInfo_mgrs_grid(::autoware_map_msgs::msg::MapProjectorInfo & msg)
  : msg_(msg)
  {}
  Init_MapProjectorInfo_map_origin mgrs_grid(::autoware_map_msgs::msg::MapProjectorInfo::_mgrs_grid_type arg)
  {
    msg_.mgrs_grid = std::move(arg);
    return Init_MapProjectorInfo_map_origin(msg_);
  }

private:
  ::autoware_map_msgs::msg::MapProjectorInfo msg_;
};

class Init_MapProjectorInfo_vertical_datum
{
public:
  explicit Init_MapProjectorInfo_vertical_datum(::autoware_map_msgs::msg::MapProjectorInfo & msg)
  : msg_(msg)
  {}
  Init_MapProjectorInfo_mgrs_grid vertical_datum(::autoware_map_msgs::msg::MapProjectorInfo::_vertical_datum_type arg)
  {
    msg_.vertical_datum = std::move(arg);
    return Init_MapProjectorInfo_mgrs_grid(msg_);
  }

private:
  ::autoware_map_msgs::msg::MapProjectorInfo msg_;
};

class Init_MapProjectorInfo_projector_type
{
public:
  Init_MapProjectorInfo_projector_type()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MapProjectorInfo_vertical_datum projector_type(::autoware_map_msgs::msg::MapProjectorInfo::_projector_type_type arg)
  {
    msg_.projector_type = std::move(arg);
    return Init_MapProjectorInfo_vertical_datum(msg_);
  }

private:
  ::autoware_map_msgs::msg::MapProjectorInfo msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::autoware_map_msgs::msg::MapProjectorInfo>()
{
  return autoware_map_msgs::msg::builder::Init_MapProjectorInfo_projector_type();
}

}  // namespace autoware_map_msgs

#endif  // AUTOWARE_MAP_MSGS__MSG__DETAIL__MAP_PROJECTOR_INFO__BUILDER_HPP_
