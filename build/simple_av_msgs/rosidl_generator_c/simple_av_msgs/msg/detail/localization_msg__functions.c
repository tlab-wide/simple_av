// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/LocalizationMsg.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/localization_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `closest_point`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `closest_lane_names`
#include "std_msgs/msg/detail/string__functions.h"

bool
simple_av_msgs__msg__LocalizationMsg__init(simple_av_msgs__msg__LocalizationMsg * msg)
{
  if (!msg) {
    return false;
  }
  // closest_point
  if (!geometry_msgs__msg__Point__init(&msg->closest_point)) {
    simple_av_msgs__msg__LocalizationMsg__fini(msg);
    return false;
  }
  // closest_lane_names
  if (!std_msgs__msg__String__init(&msg->closest_lane_names)) {
    simple_av_msgs__msg__LocalizationMsg__fini(msg);
    return false;
  }
  // minimal_distance
  return true;
}

void
simple_av_msgs__msg__LocalizationMsg__fini(simple_av_msgs__msg__LocalizationMsg * msg)
{
  if (!msg) {
    return;
  }
  // closest_point
  geometry_msgs__msg__Point__fini(&msg->closest_point);
  // closest_lane_names
  std_msgs__msg__String__fini(&msg->closest_lane_names);
  // minimal_distance
}

bool
simple_av_msgs__msg__LocalizationMsg__are_equal(const simple_av_msgs__msg__LocalizationMsg * lhs, const simple_av_msgs__msg__LocalizationMsg * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // closest_point
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->closest_point), &(rhs->closest_point)))
  {
    return false;
  }
  // closest_lane_names
  if (!std_msgs__msg__String__are_equal(
      &(lhs->closest_lane_names), &(rhs->closest_lane_names)))
  {
    return false;
  }
  // minimal_distance
  if (lhs->minimal_distance != rhs->minimal_distance) {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__LocalizationMsg__copy(
  const simple_av_msgs__msg__LocalizationMsg * input,
  simple_av_msgs__msg__LocalizationMsg * output)
{
  if (!input || !output) {
    return false;
  }
  // closest_point
  if (!geometry_msgs__msg__Point__copy(
      &(input->closest_point), &(output->closest_point)))
  {
    return false;
  }
  // closest_lane_names
  if (!std_msgs__msg__String__copy(
      &(input->closest_lane_names), &(output->closest_lane_names)))
  {
    return false;
  }
  // minimal_distance
  output->minimal_distance = input->minimal_distance;
  return true;
}

simple_av_msgs__msg__LocalizationMsg *
simple_av_msgs__msg__LocalizationMsg__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__LocalizationMsg * msg = (simple_av_msgs__msg__LocalizationMsg *)allocator.allocate(sizeof(simple_av_msgs__msg__LocalizationMsg), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__LocalizationMsg));
  bool success = simple_av_msgs__msg__LocalizationMsg__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__LocalizationMsg__destroy(simple_av_msgs__msg__LocalizationMsg * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__LocalizationMsg__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__LocalizationMsg__Sequence__init(simple_av_msgs__msg__LocalizationMsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__LocalizationMsg * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__LocalizationMsg *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__LocalizationMsg), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__LocalizationMsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__LocalizationMsg__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
simple_av_msgs__msg__LocalizationMsg__Sequence__fini(simple_av_msgs__msg__LocalizationMsg__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      simple_av_msgs__msg__LocalizationMsg__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

simple_av_msgs__msg__LocalizationMsg__Sequence *
simple_av_msgs__msg__LocalizationMsg__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__LocalizationMsg__Sequence * array = (simple_av_msgs__msg__LocalizationMsg__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__LocalizationMsg__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__LocalizationMsg__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__LocalizationMsg__Sequence__destroy(simple_av_msgs__msg__LocalizationMsg__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__LocalizationMsg__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__LocalizationMsg__Sequence__are_equal(const simple_av_msgs__msg__LocalizationMsg__Sequence * lhs, const simple_av_msgs__msg__LocalizationMsg__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__LocalizationMsg__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__LocalizationMsg__Sequence__copy(
  const simple_av_msgs__msg__LocalizationMsg__Sequence * input,
  simple_av_msgs__msg__LocalizationMsg__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__LocalizationMsg);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__LocalizationMsg * data =
      (simple_av_msgs__msg__LocalizationMsg *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__LocalizationMsg__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__LocalizationMsg__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__LocalizationMsg__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
