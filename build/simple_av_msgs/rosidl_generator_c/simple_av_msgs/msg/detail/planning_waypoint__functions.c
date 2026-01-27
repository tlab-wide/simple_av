// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/PlanningWaypoint.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/planning_waypoint__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `waypoint`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
simple_av_msgs__msg__PlanningWaypoint__init(simple_av_msgs__msg__PlanningWaypoint * msg)
{
  if (!msg) {
    return false;
  }
  // waypoint
  if (!geometry_msgs__msg__Point__init(&msg->waypoint)) {
    simple_av_msgs__msg__PlanningWaypoint__fini(msg);
    return false;
  }
  // curve
  return true;
}

void
simple_av_msgs__msg__PlanningWaypoint__fini(simple_av_msgs__msg__PlanningWaypoint * msg)
{
  if (!msg) {
    return;
  }
  // waypoint
  geometry_msgs__msg__Point__fini(&msg->waypoint);
  // curve
}

bool
simple_av_msgs__msg__PlanningWaypoint__are_equal(const simple_av_msgs__msg__PlanningWaypoint * lhs, const simple_av_msgs__msg__PlanningWaypoint * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // waypoint
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->waypoint), &(rhs->waypoint)))
  {
    return false;
  }
  // curve
  if (lhs->curve != rhs->curve) {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__PlanningWaypoint__copy(
  const simple_av_msgs__msg__PlanningWaypoint * input,
  simple_av_msgs__msg__PlanningWaypoint * output)
{
  if (!input || !output) {
    return false;
  }
  // waypoint
  if (!geometry_msgs__msg__Point__copy(
      &(input->waypoint), &(output->waypoint)))
  {
    return false;
  }
  // curve
  output->curve = input->curve;
  return true;
}

simple_av_msgs__msg__PlanningWaypoint *
simple_av_msgs__msg__PlanningWaypoint__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningWaypoint * msg = (simple_av_msgs__msg__PlanningWaypoint *)allocator.allocate(sizeof(simple_av_msgs__msg__PlanningWaypoint), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__PlanningWaypoint));
  bool success = simple_av_msgs__msg__PlanningWaypoint__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__PlanningWaypoint__destroy(simple_av_msgs__msg__PlanningWaypoint * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__PlanningWaypoint__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__PlanningWaypoint__Sequence__init(simple_av_msgs__msg__PlanningWaypoint__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningWaypoint * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__PlanningWaypoint *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__PlanningWaypoint), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__PlanningWaypoint__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__PlanningWaypoint__fini(&data[i - 1]);
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
simple_av_msgs__msg__PlanningWaypoint__Sequence__fini(simple_av_msgs__msg__PlanningWaypoint__Sequence * array)
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
      simple_av_msgs__msg__PlanningWaypoint__fini(&array->data[i]);
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

simple_av_msgs__msg__PlanningWaypoint__Sequence *
simple_av_msgs__msg__PlanningWaypoint__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningWaypoint__Sequence * array = (simple_av_msgs__msg__PlanningWaypoint__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__PlanningWaypoint__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__PlanningWaypoint__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__PlanningWaypoint__Sequence__destroy(simple_av_msgs__msg__PlanningWaypoint__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__PlanningWaypoint__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__PlanningWaypoint__Sequence__are_equal(const simple_av_msgs__msg__PlanningWaypoint__Sequence * lhs, const simple_av_msgs__msg__PlanningWaypoint__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__PlanningWaypoint__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__PlanningWaypoint__Sequence__copy(
  const simple_av_msgs__msg__PlanningWaypoint__Sequence * input,
  simple_av_msgs__msg__PlanningWaypoint__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__PlanningWaypoint);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__PlanningWaypoint * data =
      (simple_av_msgs__msg__PlanningWaypoint *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__PlanningWaypoint__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__PlanningWaypoint__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__PlanningWaypoint__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
