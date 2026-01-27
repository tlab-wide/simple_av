// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from autoware_map_msgs:msg/LaneletMapMetaData.idl
// generated code does not contain a copyright notice
#include "autoware_map_msgs/msg/detail/lanelet_map_meta_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `metadata_list`
#include "autoware_map_msgs/msg/detail/lanelet_map_cell_meta_data__functions.h"

bool
autoware_map_msgs__msg__LaneletMapMetaData__init(autoware_map_msgs__msg__LaneletMapMetaData * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    autoware_map_msgs__msg__LaneletMapMetaData__fini(msg);
    return false;
  }
  // metadata_list
  if (!autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__init(&msg->metadata_list, 0)) {
    autoware_map_msgs__msg__LaneletMapMetaData__fini(msg);
    return false;
  }
  return true;
}

void
autoware_map_msgs__msg__LaneletMapMetaData__fini(autoware_map_msgs__msg__LaneletMapMetaData * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // metadata_list
  autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__fini(&msg->metadata_list);
}

bool
autoware_map_msgs__msg__LaneletMapMetaData__are_equal(const autoware_map_msgs__msg__LaneletMapMetaData * lhs, const autoware_map_msgs__msg__LaneletMapMetaData * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // metadata_list
  if (!autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__are_equal(
      &(lhs->metadata_list), &(rhs->metadata_list)))
  {
    return false;
  }
  return true;
}

bool
autoware_map_msgs__msg__LaneletMapMetaData__copy(
  const autoware_map_msgs__msg__LaneletMapMetaData * input,
  autoware_map_msgs__msg__LaneletMapMetaData * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // metadata_list
  if (!autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__copy(
      &(input->metadata_list), &(output->metadata_list)))
  {
    return false;
  }
  return true;
}

autoware_map_msgs__msg__LaneletMapMetaData *
autoware_map_msgs__msg__LaneletMapMetaData__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_map_msgs__msg__LaneletMapMetaData * msg = (autoware_map_msgs__msg__LaneletMapMetaData *)allocator.allocate(sizeof(autoware_map_msgs__msg__LaneletMapMetaData), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(autoware_map_msgs__msg__LaneletMapMetaData));
  bool success = autoware_map_msgs__msg__LaneletMapMetaData__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
autoware_map_msgs__msg__LaneletMapMetaData__destroy(autoware_map_msgs__msg__LaneletMapMetaData * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    autoware_map_msgs__msg__LaneletMapMetaData__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
autoware_map_msgs__msg__LaneletMapMetaData__Sequence__init(autoware_map_msgs__msg__LaneletMapMetaData__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_map_msgs__msg__LaneletMapMetaData * data = NULL;

  if (size) {
    data = (autoware_map_msgs__msg__LaneletMapMetaData *)allocator.zero_allocate(size, sizeof(autoware_map_msgs__msg__LaneletMapMetaData), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = autoware_map_msgs__msg__LaneletMapMetaData__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        autoware_map_msgs__msg__LaneletMapMetaData__fini(&data[i - 1]);
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
autoware_map_msgs__msg__LaneletMapMetaData__Sequence__fini(autoware_map_msgs__msg__LaneletMapMetaData__Sequence * array)
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
      autoware_map_msgs__msg__LaneletMapMetaData__fini(&array->data[i]);
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

autoware_map_msgs__msg__LaneletMapMetaData__Sequence *
autoware_map_msgs__msg__LaneletMapMetaData__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_map_msgs__msg__LaneletMapMetaData__Sequence * array = (autoware_map_msgs__msg__LaneletMapMetaData__Sequence *)allocator.allocate(sizeof(autoware_map_msgs__msg__LaneletMapMetaData__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = autoware_map_msgs__msg__LaneletMapMetaData__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
autoware_map_msgs__msg__LaneletMapMetaData__Sequence__destroy(autoware_map_msgs__msg__LaneletMapMetaData__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    autoware_map_msgs__msg__LaneletMapMetaData__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
autoware_map_msgs__msg__LaneletMapMetaData__Sequence__are_equal(const autoware_map_msgs__msg__LaneletMapMetaData__Sequence * lhs, const autoware_map_msgs__msg__LaneletMapMetaData__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!autoware_map_msgs__msg__LaneletMapMetaData__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
autoware_map_msgs__msg__LaneletMapMetaData__Sequence__copy(
  const autoware_map_msgs__msg__LaneletMapMetaData__Sequence * input,
  autoware_map_msgs__msg__LaneletMapMetaData__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(autoware_map_msgs__msg__LaneletMapMetaData);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    autoware_map_msgs__msg__LaneletMapMetaData * data =
      (autoware_map_msgs__msg__LaneletMapMetaData *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!autoware_map_msgs__msg__LaneletMapMetaData__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          autoware_map_msgs__msg__LaneletMapMetaData__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!autoware_map_msgs__msg__LaneletMapMetaData__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
