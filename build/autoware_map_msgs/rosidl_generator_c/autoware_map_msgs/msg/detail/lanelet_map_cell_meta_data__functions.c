// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from autoware_map_msgs:msg/LaneletMapCellMetaData.idl
// generated code does not contain a copyright notice
#include "autoware_map_msgs/msg/detail/lanelet_map_cell_meta_data__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `cell_id`
#include "rosidl_runtime_c/string_functions.h"

bool
autoware_map_msgs__msg__LaneletMapCellMetaData__init(autoware_map_msgs__msg__LaneletMapCellMetaData * msg)
{
  if (!msg) {
    return false;
  }
  // cell_id
  if (!rosidl_runtime_c__String__init(&msg->cell_id)) {
    autoware_map_msgs__msg__LaneletMapCellMetaData__fini(msg);
    return false;
  }
  // min_x
  // max_x
  // min_y
  // max_y
  return true;
}

void
autoware_map_msgs__msg__LaneletMapCellMetaData__fini(autoware_map_msgs__msg__LaneletMapCellMetaData * msg)
{
  if (!msg) {
    return;
  }
  // cell_id
  rosidl_runtime_c__String__fini(&msg->cell_id);
  // min_x
  // max_x
  // min_y
  // max_y
}

bool
autoware_map_msgs__msg__LaneletMapCellMetaData__are_equal(const autoware_map_msgs__msg__LaneletMapCellMetaData * lhs, const autoware_map_msgs__msg__LaneletMapCellMetaData * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // cell_id
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->cell_id), &(rhs->cell_id)))
  {
    return false;
  }
  // min_x
  if (lhs->min_x != rhs->min_x) {
    return false;
  }
  // max_x
  if (lhs->max_x != rhs->max_x) {
    return false;
  }
  // min_y
  if (lhs->min_y != rhs->min_y) {
    return false;
  }
  // max_y
  if (lhs->max_y != rhs->max_y) {
    return false;
  }
  return true;
}

bool
autoware_map_msgs__msg__LaneletMapCellMetaData__copy(
  const autoware_map_msgs__msg__LaneletMapCellMetaData * input,
  autoware_map_msgs__msg__LaneletMapCellMetaData * output)
{
  if (!input || !output) {
    return false;
  }
  // cell_id
  if (!rosidl_runtime_c__String__copy(
      &(input->cell_id), &(output->cell_id)))
  {
    return false;
  }
  // min_x
  output->min_x = input->min_x;
  // max_x
  output->max_x = input->max_x;
  // min_y
  output->min_y = input->min_y;
  // max_y
  output->max_y = input->max_y;
  return true;
}

autoware_map_msgs__msg__LaneletMapCellMetaData *
autoware_map_msgs__msg__LaneletMapCellMetaData__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_map_msgs__msg__LaneletMapCellMetaData * msg = (autoware_map_msgs__msg__LaneletMapCellMetaData *)allocator.allocate(sizeof(autoware_map_msgs__msg__LaneletMapCellMetaData), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(autoware_map_msgs__msg__LaneletMapCellMetaData));
  bool success = autoware_map_msgs__msg__LaneletMapCellMetaData__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
autoware_map_msgs__msg__LaneletMapCellMetaData__destroy(autoware_map_msgs__msg__LaneletMapCellMetaData * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    autoware_map_msgs__msg__LaneletMapCellMetaData__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__init(autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_map_msgs__msg__LaneletMapCellMetaData * data = NULL;

  if (size) {
    data = (autoware_map_msgs__msg__LaneletMapCellMetaData *)allocator.zero_allocate(size, sizeof(autoware_map_msgs__msg__LaneletMapCellMetaData), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = autoware_map_msgs__msg__LaneletMapCellMetaData__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        autoware_map_msgs__msg__LaneletMapCellMetaData__fini(&data[i - 1]);
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
autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__fini(autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence * array)
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
      autoware_map_msgs__msg__LaneletMapCellMetaData__fini(&array->data[i]);
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

autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence *
autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence * array = (autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence *)allocator.allocate(sizeof(autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__destroy(autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__are_equal(const autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence * lhs, const autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!autoware_map_msgs__msg__LaneletMapCellMetaData__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence__copy(
  const autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence * input,
  autoware_map_msgs__msg__LaneletMapCellMetaData__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(autoware_map_msgs__msg__LaneletMapCellMetaData);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    autoware_map_msgs__msg__LaneletMapCellMetaData * data =
      (autoware_map_msgs__msg__LaneletMapCellMetaData *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!autoware_map_msgs__msg__LaneletMapCellMetaData__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          autoware_map_msgs__msg__LaneletMapCellMetaData__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!autoware_map_msgs__msg__LaneletMapCellMetaData__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
