// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/PlanningPathPlanningMsg.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/planning_path_planning_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `look_ahead_point`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
simple_av_msgs__msg__PlanningPathPlanningMsg__init(simple_av_msgs__msg__PlanningPathPlanningMsg * msg)
{
  if (!msg) {
    return false;
  }
  // look_ahead_point
  if (!geometry_msgs__msg__Point__init(&msg->look_ahead_point)) {
    simple_av_msgs__msg__PlanningPathPlanningMsg__fini(msg);
    return false;
  }
  // speed_limit
  return true;
}

void
simple_av_msgs__msg__PlanningPathPlanningMsg__fini(simple_av_msgs__msg__PlanningPathPlanningMsg * msg)
{
  if (!msg) {
    return;
  }
  // look_ahead_point
  geometry_msgs__msg__Point__fini(&msg->look_ahead_point);
  // speed_limit
}

bool
simple_av_msgs__msg__PlanningPathPlanningMsg__are_equal(const simple_av_msgs__msg__PlanningPathPlanningMsg * lhs, const simple_av_msgs__msg__PlanningPathPlanningMsg * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // look_ahead_point
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->look_ahead_point), &(rhs->look_ahead_point)))
  {
    return false;
  }
  // speed_limit
  if (lhs->speed_limit != rhs->speed_limit) {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__PlanningPathPlanningMsg__copy(
  const simple_av_msgs__msg__PlanningPathPlanningMsg * input,
  simple_av_msgs__msg__PlanningPathPlanningMsg * output)
{
  if (!input || !output) {
    return false;
  }
  // look_ahead_point
  if (!geometry_msgs__msg__Point__copy(
      &(input->look_ahead_point), &(output->look_ahead_point)))
  {
    return false;
  }
  // speed_limit
  output->speed_limit = input->speed_limit;
  return true;
}

simple_av_msgs__msg__PlanningPathPlanningMsg *
simple_av_msgs__msg__PlanningPathPlanningMsg__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningPathPlanningMsg * msg = (simple_av_msgs__msg__PlanningPathPlanningMsg *)allocator.allocate(sizeof(simple_av_msgs__msg__PlanningPathPlanningMsg), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__PlanningPathPlanningMsg));
  bool success = simple_av_msgs__msg__PlanningPathPlanningMsg__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__PlanningPathPlanningMsg__destroy(simple_av_msgs__msg__PlanningPathPlanningMsg * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__PlanningPathPlanningMsg__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence__init(simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningPathPlanningMsg * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__PlanningPathPlanningMsg *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__PlanningPathPlanningMsg), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__PlanningPathPlanningMsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__PlanningPathPlanningMsg__fini(&data[i - 1]);
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
simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence__fini(simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence * array)
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
      simple_av_msgs__msg__PlanningPathPlanningMsg__fini(&array->data[i]);
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

simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence *
simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence * array = (simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence__destroy(simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence__are_equal(const simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence * lhs, const simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__PlanningPathPlanningMsg__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence__copy(
  const simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence * input,
  simple_av_msgs__msg__PlanningPathPlanningMsg__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__PlanningPathPlanningMsg);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__PlanningPathPlanningMsg * data =
      (simple_av_msgs__msg__PlanningPathPlanningMsg *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__PlanningPathPlanningMsg__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__PlanningPathPlanningMsg__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__PlanningPathPlanningMsg__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
