// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/TrafficSignalsArray.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/traffic_signals_array__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `v2i_traffic_signals_id`
// Member `v2i_traffic_signals_colors`
#include "rosidl_runtime_c/primitives_sequence_functions.h"

bool
simple_av_msgs__msg__TrafficSignalsArray__init(simple_av_msgs__msg__TrafficSignalsArray * msg)
{
  if (!msg) {
    return false;
  }
  // v2i_traffic_signals_id
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->v2i_traffic_signals_id, 0)) {
    simple_av_msgs__msg__TrafficSignalsArray__fini(msg);
    return false;
  }
  // v2i_traffic_signals_colors
  if (!rosidl_runtime_c__int32__Sequence__init(&msg->v2i_traffic_signals_colors, 0)) {
    simple_av_msgs__msg__TrafficSignalsArray__fini(msg);
    return false;
  }
  return true;
}

void
simple_av_msgs__msg__TrafficSignalsArray__fini(simple_av_msgs__msg__TrafficSignalsArray * msg)
{
  if (!msg) {
    return;
  }
  // v2i_traffic_signals_id
  rosidl_runtime_c__int32__Sequence__fini(&msg->v2i_traffic_signals_id);
  // v2i_traffic_signals_colors
  rosidl_runtime_c__int32__Sequence__fini(&msg->v2i_traffic_signals_colors);
}

bool
simple_av_msgs__msg__TrafficSignalsArray__are_equal(const simple_av_msgs__msg__TrafficSignalsArray * lhs, const simple_av_msgs__msg__TrafficSignalsArray * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // v2i_traffic_signals_id
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->v2i_traffic_signals_id), &(rhs->v2i_traffic_signals_id)))
  {
    return false;
  }
  // v2i_traffic_signals_colors
  if (!rosidl_runtime_c__int32__Sequence__are_equal(
      &(lhs->v2i_traffic_signals_colors), &(rhs->v2i_traffic_signals_colors)))
  {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__TrafficSignalsArray__copy(
  const simple_av_msgs__msg__TrafficSignalsArray * input,
  simple_av_msgs__msg__TrafficSignalsArray * output)
{
  if (!input || !output) {
    return false;
  }
  // v2i_traffic_signals_id
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->v2i_traffic_signals_id), &(output->v2i_traffic_signals_id)))
  {
    return false;
  }
  // v2i_traffic_signals_colors
  if (!rosidl_runtime_c__int32__Sequence__copy(
      &(input->v2i_traffic_signals_colors), &(output->v2i_traffic_signals_colors)))
  {
    return false;
  }
  return true;
}

simple_av_msgs__msg__TrafficSignalsArray *
simple_av_msgs__msg__TrafficSignalsArray__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__TrafficSignalsArray * msg = (simple_av_msgs__msg__TrafficSignalsArray *)allocator.allocate(sizeof(simple_av_msgs__msg__TrafficSignalsArray), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__TrafficSignalsArray));
  bool success = simple_av_msgs__msg__TrafficSignalsArray__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__TrafficSignalsArray__destroy(simple_av_msgs__msg__TrafficSignalsArray * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__TrafficSignalsArray__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__TrafficSignalsArray__Sequence__init(simple_av_msgs__msg__TrafficSignalsArray__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__TrafficSignalsArray * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__TrafficSignalsArray *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__TrafficSignalsArray), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__TrafficSignalsArray__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__TrafficSignalsArray__fini(&data[i - 1]);
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
simple_av_msgs__msg__TrafficSignalsArray__Sequence__fini(simple_av_msgs__msg__TrafficSignalsArray__Sequence * array)
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
      simple_av_msgs__msg__TrafficSignalsArray__fini(&array->data[i]);
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

simple_av_msgs__msg__TrafficSignalsArray__Sequence *
simple_av_msgs__msg__TrafficSignalsArray__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__TrafficSignalsArray__Sequence * array = (simple_av_msgs__msg__TrafficSignalsArray__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__TrafficSignalsArray__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__TrafficSignalsArray__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__TrafficSignalsArray__Sequence__destroy(simple_av_msgs__msg__TrafficSignalsArray__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__TrafficSignalsArray__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__TrafficSignalsArray__Sequence__are_equal(const simple_av_msgs__msg__TrafficSignalsArray__Sequence * lhs, const simple_av_msgs__msg__TrafficSignalsArray__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__TrafficSignalsArray__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__TrafficSignalsArray__Sequence__copy(
  const simple_av_msgs__msg__TrafficSignalsArray__Sequence * input,
  simple_av_msgs__msg__TrafficSignalsArray__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__TrafficSignalsArray);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__TrafficSignalsArray * data =
      (simple_av_msgs__msg__TrafficSignalsArray *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__TrafficSignalsArray__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__TrafficSignalsArray__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__TrafficSignalsArray__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
