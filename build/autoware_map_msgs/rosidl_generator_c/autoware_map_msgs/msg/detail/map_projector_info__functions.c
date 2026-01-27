// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from autoware_map_msgs:msg/MapProjectorInfo.idl
// generated code does not contain a copyright notice
#include "autoware_map_msgs/msg/detail/map_projector_info__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `projector_type`
// Member `vertical_datum`
// Member `mgrs_grid`
#include "rosidl_runtime_c/string_functions.h"
// Member `map_origin`
#include "geographic_msgs/msg/detail/geo_point__functions.h"

bool
autoware_map_msgs__msg__MapProjectorInfo__init(autoware_map_msgs__msg__MapProjectorInfo * msg)
{
  if (!msg) {
    return false;
  }
  // projector_type
  if (!rosidl_runtime_c__String__init(&msg->projector_type)) {
    autoware_map_msgs__msg__MapProjectorInfo__fini(msg);
    return false;
  }
  // vertical_datum
  if (!rosidl_runtime_c__String__init(&msg->vertical_datum)) {
    autoware_map_msgs__msg__MapProjectorInfo__fini(msg);
    return false;
  }
  // mgrs_grid
  if (!rosidl_runtime_c__String__init(&msg->mgrs_grid)) {
    autoware_map_msgs__msg__MapProjectorInfo__fini(msg);
    return false;
  }
  // map_origin
  if (!geographic_msgs__msg__GeoPoint__init(&msg->map_origin)) {
    autoware_map_msgs__msg__MapProjectorInfo__fini(msg);
    return false;
  }
  // scale_factor
  return true;
}

void
autoware_map_msgs__msg__MapProjectorInfo__fini(autoware_map_msgs__msg__MapProjectorInfo * msg)
{
  if (!msg) {
    return;
  }
  // projector_type
  rosidl_runtime_c__String__fini(&msg->projector_type);
  // vertical_datum
  rosidl_runtime_c__String__fini(&msg->vertical_datum);
  // mgrs_grid
  rosidl_runtime_c__String__fini(&msg->mgrs_grid);
  // map_origin
  geographic_msgs__msg__GeoPoint__fini(&msg->map_origin);
  // scale_factor
}

bool
autoware_map_msgs__msg__MapProjectorInfo__are_equal(const autoware_map_msgs__msg__MapProjectorInfo * lhs, const autoware_map_msgs__msg__MapProjectorInfo * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // projector_type
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->projector_type), &(rhs->projector_type)))
  {
    return false;
  }
  // vertical_datum
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->vertical_datum), &(rhs->vertical_datum)))
  {
    return false;
  }
  // mgrs_grid
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->mgrs_grid), &(rhs->mgrs_grid)))
  {
    return false;
  }
  // map_origin
  if (!geographic_msgs__msg__GeoPoint__are_equal(
      &(lhs->map_origin), &(rhs->map_origin)))
  {
    return false;
  }
  // scale_factor
  if (lhs->scale_factor != rhs->scale_factor) {
    return false;
  }
  return true;
}

bool
autoware_map_msgs__msg__MapProjectorInfo__copy(
  const autoware_map_msgs__msg__MapProjectorInfo * input,
  autoware_map_msgs__msg__MapProjectorInfo * output)
{
  if (!input || !output) {
    return false;
  }
  // projector_type
  if (!rosidl_runtime_c__String__copy(
      &(input->projector_type), &(output->projector_type)))
  {
    return false;
  }
  // vertical_datum
  if (!rosidl_runtime_c__String__copy(
      &(input->vertical_datum), &(output->vertical_datum)))
  {
    return false;
  }
  // mgrs_grid
  if (!rosidl_runtime_c__String__copy(
      &(input->mgrs_grid), &(output->mgrs_grid)))
  {
    return false;
  }
  // map_origin
  if (!geographic_msgs__msg__GeoPoint__copy(
      &(input->map_origin), &(output->map_origin)))
  {
    return false;
  }
  // scale_factor
  output->scale_factor = input->scale_factor;
  return true;
}

autoware_map_msgs__msg__MapProjectorInfo *
autoware_map_msgs__msg__MapProjectorInfo__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_map_msgs__msg__MapProjectorInfo * msg = (autoware_map_msgs__msg__MapProjectorInfo *)allocator.allocate(sizeof(autoware_map_msgs__msg__MapProjectorInfo), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(autoware_map_msgs__msg__MapProjectorInfo));
  bool success = autoware_map_msgs__msg__MapProjectorInfo__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
autoware_map_msgs__msg__MapProjectorInfo__destroy(autoware_map_msgs__msg__MapProjectorInfo * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    autoware_map_msgs__msg__MapProjectorInfo__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
autoware_map_msgs__msg__MapProjectorInfo__Sequence__init(autoware_map_msgs__msg__MapProjectorInfo__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_map_msgs__msg__MapProjectorInfo * data = NULL;

  if (size) {
    data = (autoware_map_msgs__msg__MapProjectorInfo *)allocator.zero_allocate(size, sizeof(autoware_map_msgs__msg__MapProjectorInfo), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = autoware_map_msgs__msg__MapProjectorInfo__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        autoware_map_msgs__msg__MapProjectorInfo__fini(&data[i - 1]);
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
autoware_map_msgs__msg__MapProjectorInfo__Sequence__fini(autoware_map_msgs__msg__MapProjectorInfo__Sequence * array)
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
      autoware_map_msgs__msg__MapProjectorInfo__fini(&array->data[i]);
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

autoware_map_msgs__msg__MapProjectorInfo__Sequence *
autoware_map_msgs__msg__MapProjectorInfo__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_map_msgs__msg__MapProjectorInfo__Sequence * array = (autoware_map_msgs__msg__MapProjectorInfo__Sequence *)allocator.allocate(sizeof(autoware_map_msgs__msg__MapProjectorInfo__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = autoware_map_msgs__msg__MapProjectorInfo__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
autoware_map_msgs__msg__MapProjectorInfo__Sequence__destroy(autoware_map_msgs__msg__MapProjectorInfo__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    autoware_map_msgs__msg__MapProjectorInfo__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
autoware_map_msgs__msg__MapProjectorInfo__Sequence__are_equal(const autoware_map_msgs__msg__MapProjectorInfo__Sequence * lhs, const autoware_map_msgs__msg__MapProjectorInfo__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!autoware_map_msgs__msg__MapProjectorInfo__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
autoware_map_msgs__msg__MapProjectorInfo__Sequence__copy(
  const autoware_map_msgs__msg__MapProjectorInfo__Sequence * input,
  autoware_map_msgs__msg__MapProjectorInfo__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(autoware_map_msgs__msg__MapProjectorInfo);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    autoware_map_msgs__msg__MapProjectorInfo * data =
      (autoware_map_msgs__msg__MapProjectorInfo *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!autoware_map_msgs__msg__MapProjectorInfo__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          autoware_map_msgs__msg__MapProjectorInfo__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!autoware_map_msgs__msg__MapProjectorInfo__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
