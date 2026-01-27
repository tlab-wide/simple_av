// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/PlanningMotionPlanningMsg.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/planning_motion_planning_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `stop_point`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `status`
// Member `stop_reason`
#include "std_msgs/msg/detail/string__functions.h"

bool
simple_av_msgs__msg__PlanningMotionPlanningMsg__init(simple_av_msgs__msg__PlanningMotionPlanningMsg * msg)
{
  if (!msg) {
    return false;
  }
  // stop_point
  if (!geometry_msgs__msg__Point__init(&msg->stop_point)) {
    simple_av_msgs__msg__PlanningMotionPlanningMsg__fini(msg);
    return false;
  }
  // status
  if (!std_msgs__msg__String__init(&msg->status)) {
    simple_av_msgs__msg__PlanningMotionPlanningMsg__fini(msg);
    return false;
  }
  // stop_reason
  if (!std_msgs__msg__String__init(&msg->stop_reason)) {
    simple_av_msgs__msg__PlanningMotionPlanningMsg__fini(msg);
    return false;
  }
  return true;
}

void
simple_av_msgs__msg__PlanningMotionPlanningMsg__fini(simple_av_msgs__msg__PlanningMotionPlanningMsg * msg)
{
  if (!msg) {
    return;
  }
  // stop_point
  geometry_msgs__msg__Point__fini(&msg->stop_point);
  // status
  std_msgs__msg__String__fini(&msg->status);
  // stop_reason
  std_msgs__msg__String__fini(&msg->stop_reason);
}

bool
simple_av_msgs__msg__PlanningMotionPlanningMsg__are_equal(const simple_av_msgs__msg__PlanningMotionPlanningMsg * lhs, const simple_av_msgs__msg__PlanningMotionPlanningMsg * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // stop_point
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->stop_point), &(rhs->stop_point)))
  {
    return false;
  }
  // status
  if (!std_msgs__msg__String__are_equal(
      &(lhs->status), &(rhs->status)))
  {
    return false;
  }
  // stop_reason
  if (!std_msgs__msg__String__are_equal(
      &(lhs->stop_reason), &(rhs->stop_reason)))
  {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__PlanningMotionPlanningMsg__copy(
  const simple_av_msgs__msg__PlanningMotionPlanningMsg * input,
  simple_av_msgs__msg__PlanningMotionPlanningMsg * output)
{
  if (!input || !output) {
    return false;
  }
  // stop_point
  if (!geometry_msgs__msg__Point__copy(
      &(input->stop_point), &(output->stop_point)))
  {
    return false;
  }
  // status
  if (!std_msgs__msg__String__copy(
      &(input->status), &(output->status)))
  {
    return false;
  }
  // stop_reason
  if (!std_msgs__msg__String__copy(
      &(input->stop_reason), &(output->stop_reason)))
  {
    return false;
  }
  return true;
}

simple_av_msgs__msg__PlanningMotionPlanningMsg *
simple_av_msgs__msg__PlanningMotionPlanningMsg__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningMotionPlanningMsg * msg = (simple_av_msgs__msg__PlanningMotionPlanningMsg *)allocator.allocate(sizeof(simple_av_msgs__msg__PlanningMotionPlanningMsg), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__PlanningMotionPlanningMsg));
  bool success = simple_av_msgs__msg__PlanningMotionPlanningMsg__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__PlanningMotionPlanningMsg__destroy(simple_av_msgs__msg__PlanningMotionPlanningMsg * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__PlanningMotionPlanningMsg__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence__init(simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningMotionPlanningMsg * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__PlanningMotionPlanningMsg *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__PlanningMotionPlanningMsg), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__PlanningMotionPlanningMsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__PlanningMotionPlanningMsg__fini(&data[i - 1]);
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
simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence__fini(simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence * array)
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
      simple_av_msgs__msg__PlanningMotionPlanningMsg__fini(&array->data[i]);
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

simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence *
simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence * array = (simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence__destroy(simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence__are_equal(const simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence * lhs, const simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__PlanningMotionPlanningMsg__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence__copy(
  const simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence * input,
  simple_av_msgs__msg__PlanningMotionPlanningMsg__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__PlanningMotionPlanningMsg);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__PlanningMotionPlanningMsg * data =
      (simple_av_msgs__msg__PlanningMotionPlanningMsg *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__PlanningMotionPlanningMsg__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__PlanningMotionPlanningMsg__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__PlanningMotionPlanningMsg__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
