// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from autoware_internal_debug_msgs:msg/ProcessingTimeNode.idl
// generated code does not contain a copyright notice
#include "autoware_internal_debug_msgs/msg/detail/processing_time_node__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `name`
// Member `comment`
#include "rosidl_runtime_c/string_functions.h"

bool
autoware_internal_debug_msgs__msg__ProcessingTimeNode__init(autoware_internal_debug_msgs__msg__ProcessingTimeNode * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // name
  if (!rosidl_runtime_c__String__init(&msg->name)) {
    autoware_internal_debug_msgs__msg__ProcessingTimeNode__fini(msg);
    return false;
  }
  // processing_time
  // parent_id
  // comment
  if (!rosidl_runtime_c__String__init(&msg->comment)) {
    autoware_internal_debug_msgs__msg__ProcessingTimeNode__fini(msg);
    return false;
  }
  return true;
}

void
autoware_internal_debug_msgs__msg__ProcessingTimeNode__fini(autoware_internal_debug_msgs__msg__ProcessingTimeNode * msg)
{
  if (!msg) {
    return;
  }
  // id
  // name
  rosidl_runtime_c__String__fini(&msg->name);
  // processing_time
  // parent_id
  // comment
  rosidl_runtime_c__String__fini(&msg->comment);
}

bool
autoware_internal_debug_msgs__msg__ProcessingTimeNode__are_equal(const autoware_internal_debug_msgs__msg__ProcessingTimeNode * lhs, const autoware_internal_debug_msgs__msg__ProcessingTimeNode * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->name), &(rhs->name)))
  {
    return false;
  }
  // processing_time
  if (lhs->processing_time != rhs->processing_time) {
    return false;
  }
  // parent_id
  if (lhs->parent_id != rhs->parent_id) {
    return false;
  }
  // comment
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->comment), &(rhs->comment)))
  {
    return false;
  }
  return true;
}

bool
autoware_internal_debug_msgs__msg__ProcessingTimeNode__copy(
  const autoware_internal_debug_msgs__msg__ProcessingTimeNode * input,
  autoware_internal_debug_msgs__msg__ProcessingTimeNode * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // name
  if (!rosidl_runtime_c__String__copy(
      &(input->name), &(output->name)))
  {
    return false;
  }
  // processing_time
  output->processing_time = input->processing_time;
  // parent_id
  output->parent_id = input->parent_id;
  // comment
  if (!rosidl_runtime_c__String__copy(
      &(input->comment), &(output->comment)))
  {
    return false;
  }
  return true;
}

autoware_internal_debug_msgs__msg__ProcessingTimeNode *
autoware_internal_debug_msgs__msg__ProcessingTimeNode__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_internal_debug_msgs__msg__ProcessingTimeNode * msg = (autoware_internal_debug_msgs__msg__ProcessingTimeNode *)allocator.allocate(sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeNode), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeNode));
  bool success = autoware_internal_debug_msgs__msg__ProcessingTimeNode__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
autoware_internal_debug_msgs__msg__ProcessingTimeNode__destroy(autoware_internal_debug_msgs__msg__ProcessingTimeNode * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    autoware_internal_debug_msgs__msg__ProcessingTimeNode__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__init(autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_internal_debug_msgs__msg__ProcessingTimeNode * data = NULL;

  if (size) {
    data = (autoware_internal_debug_msgs__msg__ProcessingTimeNode *)allocator.zero_allocate(size, sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeNode), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = autoware_internal_debug_msgs__msg__ProcessingTimeNode__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        autoware_internal_debug_msgs__msg__ProcessingTimeNode__fini(&data[i - 1]);
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
autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__fini(autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * array)
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
      autoware_internal_debug_msgs__msg__ProcessingTimeNode__fini(&array->data[i]);
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

autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence *
autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * array = (autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence *)allocator.allocate(sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__destroy(autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__are_equal(const autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * lhs, const autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!autoware_internal_debug_msgs__msg__ProcessingTimeNode__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence__copy(
  const autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * input,
  autoware_internal_debug_msgs__msg__ProcessingTimeNode__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(autoware_internal_debug_msgs__msg__ProcessingTimeNode);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    autoware_internal_debug_msgs__msg__ProcessingTimeNode * data =
      (autoware_internal_debug_msgs__msg__ProcessingTimeNode *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!autoware_internal_debug_msgs__msg__ProcessingTimeNode__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          autoware_internal_debug_msgs__msg__ProcessingTimeNode__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!autoware_internal_debug_msgs__msg__ProcessingTimeNode__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
