// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/CollisionPredictionInfo.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/collision_prediction_info__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `object_position`
#include "geometry_msgs/msg/detail/point__functions.h"

bool
simple_av_msgs__msg__CollisionPredictionInfo__init(simple_av_msgs__msg__CollisionPredictionInfo * msg)
{
  if (!msg) {
    return false;
  }
  // object_position
  if (!geometry_msgs__msg__Point__init(&msg->object_position)) {
    simple_av_msgs__msg__CollisionPredictionInfo__fini(msg);
    return false;
  }
  // time_to_collision
  // object_label
  // object_velocity
  // collision_detected
  return true;
}

void
simple_av_msgs__msg__CollisionPredictionInfo__fini(simple_av_msgs__msg__CollisionPredictionInfo * msg)
{
  if (!msg) {
    return;
  }
  // object_position
  geometry_msgs__msg__Point__fini(&msg->object_position);
  // time_to_collision
  // object_label
  // object_velocity
  // collision_detected
}

bool
simple_av_msgs__msg__CollisionPredictionInfo__are_equal(const simple_av_msgs__msg__CollisionPredictionInfo * lhs, const simple_av_msgs__msg__CollisionPredictionInfo * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // object_position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->object_position), &(rhs->object_position)))
  {
    return false;
  }
  // time_to_collision
  if (lhs->time_to_collision != rhs->time_to_collision) {
    return false;
  }
  // object_label
  if (lhs->object_label != rhs->object_label) {
    return false;
  }
  // object_velocity
  if (lhs->object_velocity != rhs->object_velocity) {
    return false;
  }
  // collision_detected
  if (lhs->collision_detected != rhs->collision_detected) {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__CollisionPredictionInfo__copy(
  const simple_av_msgs__msg__CollisionPredictionInfo * input,
  simple_av_msgs__msg__CollisionPredictionInfo * output)
{
  if (!input || !output) {
    return false;
  }
  // object_position
  if (!geometry_msgs__msg__Point__copy(
      &(input->object_position), &(output->object_position)))
  {
    return false;
  }
  // time_to_collision
  output->time_to_collision = input->time_to_collision;
  // object_label
  output->object_label = input->object_label;
  // object_velocity
  output->object_velocity = input->object_velocity;
  // collision_detected
  output->collision_detected = input->collision_detected;
  return true;
}

simple_av_msgs__msg__CollisionPredictionInfo *
simple_av_msgs__msg__CollisionPredictionInfo__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__CollisionPredictionInfo * msg = (simple_av_msgs__msg__CollisionPredictionInfo *)allocator.allocate(sizeof(simple_av_msgs__msg__CollisionPredictionInfo), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__CollisionPredictionInfo));
  bool success = simple_av_msgs__msg__CollisionPredictionInfo__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__CollisionPredictionInfo__destroy(simple_av_msgs__msg__CollisionPredictionInfo * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__CollisionPredictionInfo__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__CollisionPredictionInfo__Sequence__init(simple_av_msgs__msg__CollisionPredictionInfo__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__CollisionPredictionInfo * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__CollisionPredictionInfo *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__CollisionPredictionInfo), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__CollisionPredictionInfo__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__CollisionPredictionInfo__fini(&data[i - 1]);
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
simple_av_msgs__msg__CollisionPredictionInfo__Sequence__fini(simple_av_msgs__msg__CollisionPredictionInfo__Sequence * array)
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
      simple_av_msgs__msg__CollisionPredictionInfo__fini(&array->data[i]);
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

simple_av_msgs__msg__CollisionPredictionInfo__Sequence *
simple_av_msgs__msg__CollisionPredictionInfo__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__CollisionPredictionInfo__Sequence * array = (simple_av_msgs__msg__CollisionPredictionInfo__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__CollisionPredictionInfo__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__CollisionPredictionInfo__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__CollisionPredictionInfo__Sequence__destroy(simple_av_msgs__msg__CollisionPredictionInfo__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__CollisionPredictionInfo__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__CollisionPredictionInfo__Sequence__are_equal(const simple_av_msgs__msg__CollisionPredictionInfo__Sequence * lhs, const simple_av_msgs__msg__CollisionPredictionInfo__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__CollisionPredictionInfo__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__CollisionPredictionInfo__Sequence__copy(
  const simple_av_msgs__msg__CollisionPredictionInfo__Sequence * input,
  simple_av_msgs__msg__CollisionPredictionInfo__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__CollisionPredictionInfo);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__CollisionPredictionInfo * data =
      (simple_av_msgs__msg__CollisionPredictionInfo *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__CollisionPredictionInfo__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__CollisionPredictionInfo__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__CollisionPredictionInfo__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
