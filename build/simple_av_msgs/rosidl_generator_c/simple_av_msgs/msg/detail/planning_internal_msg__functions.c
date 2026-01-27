// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/PlanningInternalMsg.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/planning_internal_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
simple_av_msgs__msg__PlanningInternalMsg__init(simple_av_msgs__msg__PlanningInternalMsg * msg)
{
  if (!msg) {
    return false;
  }
  // is_curve_detected
  // is_end_of_path
  return true;
}

void
simple_av_msgs__msg__PlanningInternalMsg__fini(simple_av_msgs__msg__PlanningInternalMsg * msg)
{
  if (!msg) {
    return;
  }
  // is_curve_detected
  // is_end_of_path
}

bool
simple_av_msgs__msg__PlanningInternalMsg__are_equal(const simple_av_msgs__msg__PlanningInternalMsg * lhs, const simple_av_msgs__msg__PlanningInternalMsg * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // is_curve_detected
  if (lhs->is_curve_detected != rhs->is_curve_detected) {
    return false;
  }
  // is_end_of_path
  if (lhs->is_end_of_path != rhs->is_end_of_path) {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__PlanningInternalMsg__copy(
  const simple_av_msgs__msg__PlanningInternalMsg * input,
  simple_av_msgs__msg__PlanningInternalMsg * output)
{
  if (!input || !output) {
    return false;
  }
  // is_curve_detected
  output->is_curve_detected = input->is_curve_detected;
  // is_end_of_path
  output->is_end_of_path = input->is_end_of_path;
  return true;
}

simple_av_msgs__msg__PlanningInternalMsg *
simple_av_msgs__msg__PlanningInternalMsg__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningInternalMsg * msg = (simple_av_msgs__msg__PlanningInternalMsg *)allocator.allocate(sizeof(simple_av_msgs__msg__PlanningInternalMsg), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__PlanningInternalMsg));
  bool success = simple_av_msgs__msg__PlanningInternalMsg__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__PlanningInternalMsg__destroy(simple_av_msgs__msg__PlanningInternalMsg * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__PlanningInternalMsg__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__PlanningInternalMsg__Sequence__init(simple_av_msgs__msg__PlanningInternalMsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningInternalMsg * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__PlanningInternalMsg *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__PlanningInternalMsg), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__PlanningInternalMsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__PlanningInternalMsg__fini(&data[i - 1]);
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
simple_av_msgs__msg__PlanningInternalMsg__Sequence__fini(simple_av_msgs__msg__PlanningInternalMsg__Sequence * array)
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
      simple_av_msgs__msg__PlanningInternalMsg__fini(&array->data[i]);
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

simple_av_msgs__msg__PlanningInternalMsg__Sequence *
simple_av_msgs__msg__PlanningInternalMsg__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__PlanningInternalMsg__Sequence * array = (simple_av_msgs__msg__PlanningInternalMsg__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__PlanningInternalMsg__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__PlanningInternalMsg__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__PlanningInternalMsg__Sequence__destroy(simple_av_msgs__msg__PlanningInternalMsg__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__PlanningInternalMsg__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__PlanningInternalMsg__Sequence__are_equal(const simple_av_msgs__msg__PlanningInternalMsg__Sequence * lhs, const simple_av_msgs__msg__PlanningInternalMsg__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__PlanningInternalMsg__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__PlanningInternalMsg__Sequence__copy(
  const simple_av_msgs__msg__PlanningInternalMsg__Sequence * input,
  simple_av_msgs__msg__PlanningInternalMsg__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__PlanningInternalMsg);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__PlanningInternalMsg * data =
      (simple_av_msgs__msg__PlanningInternalMsg *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__PlanningInternalMsg__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__PlanningInternalMsg__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__PlanningInternalMsg__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
