// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeTree.idl
// generated code does not contain a copyright notice
#include "autoware_internal_debug_msgs/msg/detail/processing_time_tree__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `nodes`
#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__functions.h"

bool
autoware_internal_debug_msgs__msg__ProcessingTimeTree__init(autoware_internal_debug_msgs__msg__ProcessingTimeTree * msg)
{
  if (!msg) {
    return false;
  }
  // nodes
  if (!autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__init(&msg->nodes, 0)) {
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__fini(msg);
    return false;
  }
  return true;
}

void
autoware_internal_debug_msgs__msg__ProcessingTimeTree__fini(autoware_internal_debug_msgs__msg__ProcessingTimeTree * msg)
{
  if (!msg) {
    return;
  }
  // nodes
  autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__fini(&msg->nodes);
}

bool
autoware_internal_debug_msgs__msg__ProcessingTimeTree__are_equal(const autoware_internal_debug_msgs__msg__ProcessingTimeTree * lhs, const autoware_internal_debug_msgs__msg__ProcessingTimeTree * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // nodes
  if (!autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__are_equal(
      &(lhs->nodes), &(rhs->nodes)))
  {
    return false;
  }
  return true;
}

bool
autoware_internal_debug_msgs__msg__ProcessingTimeTree__copy(
  const autoware_internal_debug_msgs__msg__ProcessingTimeTree * input,
  autoware_internal_debug_msgs__msg__ProcessingTimeTree * output)
{
  if (!input || !output) {
    return false;
  }
  // nodes
  if (!autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__copy(
      &(input->nodes), &(output->nodes)))
  {
    return false;
  }
  return true;
}

autoware_internal_debug_msgs__msg__ProcessingTimeTree *
autoware_internal_debug_msgs__msg__ProcessingTimeTree__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_internal_debug_msgs__msg__ProcessingTimeTree * msg = (autoware_internal_debug_msgs__msg__ProcessingTimeTree *)allocator.allocate(sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeTree), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeTree));
  bool success = autoware_internal_debug_msgs__msg__ProcessingTimeTree__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
autoware_internal_debug_msgs__msg__ProcessingTimeTree__destroy(autoware_internal_debug_msgs__msg__ProcessingTimeTree * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence__init(autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_internal_debug_msgs__msg__ProcessingTimeTree * data = NULL;

  if (size) {
    data = (autoware_internal_debug_msgs__msg__ProcessingTimeTree *)allocator.zero_allocate(size, sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeTree), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = autoware_internal_debug_msgs__msg__ProcessingTimeTree__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        autoware_internal_debug_msgs__msg__ProcessingTimeTree__fini(&data[i - 1]);
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
autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence__fini(autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence * array)
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
      autoware_internal_debug_msgs__msg__ProcessingTimeTree__fini(&array->data[i]);
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

autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence *
autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence * array = (autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence *)allocator.allocate(sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence__destroy(autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence__are_equal(const autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence * lhs, const autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!autoware_internal_debug_msgs__msg__ProcessingTimeTree__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence__copy(
  const autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence * input,
  autoware_internal_debug_msgs__msg__ProcessingTimeTree__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeTree);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    autoware_internal_debug_msgs__msg__ProcessingTimeTree * data =
      (autoware_internal_debug_msgs__msg__ProcessingTimeTree *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!autoware_internal_debug_msgs__msg__ProcessingTimeTree__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          autoware_internal_debug_msgs__msg__ProcessingTimeTree__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!autoware_internal_debug_msgs__msg__ProcessingTimeTree__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
