// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/LocalizationIntersectionStatus.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/localization_intersection_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `intersection_name`
// Member `status`
#include "rosidl_runtime_c/string_functions.h"

bool
simple_av_msgs__msg__LocalizationIntersectionStatus__init(simple_av_msgs__msg__LocalizationIntersectionStatus * msg)
{
  if (!msg) {
    return false;
  }
  // intersection_name
  if (!rosidl_runtime_c__String__init(&msg->intersection_name)) {
    simple_av_msgs__msg__LocalizationIntersectionStatus__fini(msg);
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__init(&msg->status)) {
    simple_av_msgs__msg__LocalizationIntersectionStatus__fini(msg);
    return false;
  }
  // distance_to_intersection
  return true;
}

void
simple_av_msgs__msg__LocalizationIntersectionStatus__fini(simple_av_msgs__msg__LocalizationIntersectionStatus * msg)
{
  if (!msg) {
    return;
  }
  // intersection_name
  rosidl_runtime_c__String__fini(&msg->intersection_name);
  // status
  rosidl_runtime_c__String__fini(&msg->status);
  // distance_to_intersection
}

bool
simple_av_msgs__msg__LocalizationIntersectionStatus__are_equal(const simple_av_msgs__msg__LocalizationIntersectionStatus * lhs, const simple_av_msgs__msg__LocalizationIntersectionStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // intersection_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->intersection_name), &(rhs->intersection_name)))
  {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->status), &(rhs->status)))
  {
    return false;
  }
  // distance_to_intersection
  if (lhs->distance_to_intersection != rhs->distance_to_intersection) {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__LocalizationIntersectionStatus__copy(
  const simple_av_msgs__msg__LocalizationIntersectionStatus * input,
  simple_av_msgs__msg__LocalizationIntersectionStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // intersection_name
  if (!rosidl_runtime_c__String__copy(
      &(input->intersection_name), &(output->intersection_name)))
  {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__copy(
      &(input->status), &(output->status)))
  {
    return false;
  }
  // distance_to_intersection
  output->distance_to_intersection = input->distance_to_intersection;
  return true;
}

simple_av_msgs__msg__LocalizationIntersectionStatus *
simple_av_msgs__msg__LocalizationIntersectionStatus__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__LocalizationIntersectionStatus * msg = (simple_av_msgs__msg__LocalizationIntersectionStatus *)allocator.allocate(sizeof(simple_av_msgs__msg__LocalizationIntersectionStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__LocalizationIntersectionStatus));
  bool success = simple_av_msgs__msg__LocalizationIntersectionStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__LocalizationIntersectionStatus__destroy(simple_av_msgs__msg__LocalizationIntersectionStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__LocalizationIntersectionStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence__init(simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__LocalizationIntersectionStatus * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__LocalizationIntersectionStatus *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__LocalizationIntersectionStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__LocalizationIntersectionStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__LocalizationIntersectionStatus__fini(&data[i - 1]);
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
simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence__fini(simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence * array)
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
      simple_av_msgs__msg__LocalizationIntersectionStatus__fini(&array->data[i]);
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

simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence *
simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence * array = (simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence__destroy(simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence__are_equal(const simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence * lhs, const simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__LocalizationIntersectionStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence__copy(
  const simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence * input,
  simple_av_msgs__msg__LocalizationIntersectionStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__LocalizationIntersectionStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__LocalizationIntersectionStatus * data =
      (simple_av_msgs__msg__LocalizationIntersectionStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__LocalizationIntersectionStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__LocalizationIntersectionStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__LocalizationIntersectionStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
