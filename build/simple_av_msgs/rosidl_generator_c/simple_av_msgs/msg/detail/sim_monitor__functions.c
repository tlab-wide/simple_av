// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/SimMonitor.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/sim_monitor__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
simple_av_msgs__msg__SimMonitor__init(simple_av_msgs__msg__SimMonitor * msg)
{
  if (!msg) {
    return false;
  }
  // system_time
  // sim_time
  // sim_clock_rate
  return true;
}

void
simple_av_msgs__msg__SimMonitor__fini(simple_av_msgs__msg__SimMonitor * msg)
{
  if (!msg) {
    return;
  }
  // system_time
  // sim_time
  // sim_clock_rate
}

bool
simple_av_msgs__msg__SimMonitor__are_equal(const simple_av_msgs__msg__SimMonitor * lhs, const simple_av_msgs__msg__SimMonitor * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // system_time
  if (lhs->system_time != rhs->system_time) {
    return false;
  }
  // sim_time
  if (lhs->sim_time != rhs->sim_time) {
    return false;
  }
  // sim_clock_rate
  if (lhs->sim_clock_rate != rhs->sim_clock_rate) {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__SimMonitor__copy(
  const simple_av_msgs__msg__SimMonitor * input,
  simple_av_msgs__msg__SimMonitor * output)
{
  if (!input || !output) {
    return false;
  }
  // system_time
  output->system_time = input->system_time;
  // sim_time
  output->sim_time = input->sim_time;
  // sim_clock_rate
  output->sim_clock_rate = input->sim_clock_rate;
  return true;
}

simple_av_msgs__msg__SimMonitor *
simple_av_msgs__msg__SimMonitor__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__SimMonitor * msg = (simple_av_msgs__msg__SimMonitor *)allocator.allocate(sizeof(simple_av_msgs__msg__SimMonitor), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__SimMonitor));
  bool success = simple_av_msgs__msg__SimMonitor__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__SimMonitor__destroy(simple_av_msgs__msg__SimMonitor * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__SimMonitor__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__SimMonitor__Sequence__init(simple_av_msgs__msg__SimMonitor__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__SimMonitor * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__SimMonitor *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__SimMonitor), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__SimMonitor__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__SimMonitor__fini(&data[i - 1]);
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
simple_av_msgs__msg__SimMonitor__Sequence__fini(simple_av_msgs__msg__SimMonitor__Sequence * array)
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
      simple_av_msgs__msg__SimMonitor__fini(&array->data[i]);
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

simple_av_msgs__msg__SimMonitor__Sequence *
simple_av_msgs__msg__SimMonitor__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__SimMonitor__Sequence * array = (simple_av_msgs__msg__SimMonitor__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__SimMonitor__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__SimMonitor__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__SimMonitor__Sequence__destroy(simple_av_msgs__msg__SimMonitor__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__SimMonitor__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__SimMonitor__Sequence__are_equal(const simple_av_msgs__msg__SimMonitor__Sequence * lhs, const simple_av_msgs__msg__SimMonitor__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__SimMonitor__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__SimMonitor__Sequence__copy(
  const simple_av_msgs__msg__SimMonitor__Sequence * input,
  simple_av_msgs__msg__SimMonitor__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__SimMonitor);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__SimMonitor * data =
      (simple_av_msgs__msg__SimMonitor *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__SimMonitor__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__SimMonitor__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__SimMonitor__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
