// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from simple_av_msgs:msg/DetectedObject.idl
// generated code does not contain a copyright notice
#include "simple_av_msgs/msg/detail/detected_object__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `position`
// Member `bounding_box`
#include "geometry_msgs/msg/detail/point__functions.h"
// Member `orientation`
#include "geometry_msgs/msg/detail/quaternion__functions.h"
// Member `shape`
#include "geometry_msgs/msg/detail/vector3__functions.h"
// Member `relative_direction`
#include "std_msgs/msg/detail/string__functions.h"

bool
simple_av_msgs__msg__DetectedObject__init(simple_av_msgs__msg__DetectedObject * msg)
{
  if (!msg) {
    return false;
  }
  // is_from_rsu
  // label
  // position
  if (!geometry_msgs__msg__Point__init(&msg->position)) {
    simple_av_msgs__msg__DetectedObject__fini(msg);
    return false;
  }
  // velocity
  // orientation
  if (!geometry_msgs__msg__Quaternion__init(&msg->orientation)) {
    simple_av_msgs__msg__DetectedObject__fini(msg);
    return false;
  }
  // shape
  if (!geometry_msgs__msg__Vector3__init(&msg->shape)) {
    simple_av_msgs__msg__DetectedObject__fini(msg);
    return false;
  }
  // relative_direction
  if (!std_msgs__msg__String__init(&msg->relative_direction)) {
    simple_av_msgs__msg__DetectedObject__fini(msg);
    return false;
  }
  // bounding_box
  for (size_t i = 0; i < 4; ++i) {
    if (!geometry_msgs__msg__Point__init(&msg->bounding_box[i])) {
      simple_av_msgs__msg__DetectedObject__fini(msg);
      return false;
    }
  }
  // distance
  // nearest_object_side
  return true;
}

void
simple_av_msgs__msg__DetectedObject__fini(simple_av_msgs__msg__DetectedObject * msg)
{
  if (!msg) {
    return;
  }
  // is_from_rsu
  // label
  // position
  geometry_msgs__msg__Point__fini(&msg->position);
  // velocity
  // orientation
  geometry_msgs__msg__Quaternion__fini(&msg->orientation);
  // shape
  geometry_msgs__msg__Vector3__fini(&msg->shape);
  // relative_direction
  std_msgs__msg__String__fini(&msg->relative_direction);
  // bounding_box
  for (size_t i = 0; i < 4; ++i) {
    geometry_msgs__msg__Point__fini(&msg->bounding_box[i]);
  }
  // distance
  // nearest_object_side
}

bool
simple_av_msgs__msg__DetectedObject__are_equal(const simple_av_msgs__msg__DetectedObject * lhs, const simple_av_msgs__msg__DetectedObject * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // is_from_rsu
  if (lhs->is_from_rsu != rhs->is_from_rsu) {
    return false;
  }
  // label
  if (lhs->label != rhs->label) {
    return false;
  }
  // position
  if (!geometry_msgs__msg__Point__are_equal(
      &(lhs->position), &(rhs->position)))
  {
    return false;
  }
  // velocity
  if (lhs->velocity != rhs->velocity) {
    return false;
  }
  // orientation
  if (!geometry_msgs__msg__Quaternion__are_equal(
      &(lhs->orientation), &(rhs->orientation)))
  {
    return false;
  }
  // shape
  if (!geometry_msgs__msg__Vector3__are_equal(
      &(lhs->shape), &(rhs->shape)))
  {
    return false;
  }
  // relative_direction
  if (!std_msgs__msg__String__are_equal(
      &(lhs->relative_direction), &(rhs->relative_direction)))
  {
    return false;
  }
  // bounding_box
  for (size_t i = 0; i < 4; ++i) {
    if (!geometry_msgs__msg__Point__are_equal(
        &(lhs->bounding_box[i]), &(rhs->bounding_box[i])))
    {
      return false;
    }
  }
  // distance
  if (lhs->distance != rhs->distance) {
    return false;
  }
  // nearest_object_side
  if (lhs->nearest_object_side != rhs->nearest_object_side) {
    return false;
  }
  return true;
}

bool
simple_av_msgs__msg__DetectedObject__copy(
  const simple_av_msgs__msg__DetectedObject * input,
  simple_av_msgs__msg__DetectedObject * output)
{
  if (!input || !output) {
    return false;
  }
  // is_from_rsu
  output->is_from_rsu = input->is_from_rsu;
  // label
  output->label = input->label;
  // position
  if (!geometry_msgs__msg__Point__copy(
      &(input->position), &(output->position)))
  {
    return false;
  }
  // velocity
  output->velocity = input->velocity;
  // orientation
  if (!geometry_msgs__msg__Quaternion__copy(
      &(input->orientation), &(output->orientation)))
  {
    return false;
  }
  // shape
  if (!geometry_msgs__msg__Vector3__copy(
      &(input->shape), &(output->shape)))
  {
    return false;
  }
  // relative_direction
  if (!std_msgs__msg__String__copy(
      &(input->relative_direction), &(output->relative_direction)))
  {
    return false;
  }
  // bounding_box
  for (size_t i = 0; i < 4; ++i) {
    if (!geometry_msgs__msg__Point__copy(
        &(input->bounding_box[i]), &(output->bounding_box[i])))
    {
      return false;
    }
  }
  // distance
  output->distance = input->distance;
  // nearest_object_side
  output->nearest_object_side = input->nearest_object_side;
  return true;
}

simple_av_msgs__msg__DetectedObject *
simple_av_msgs__msg__DetectedObject__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__DetectedObject * msg = (simple_av_msgs__msg__DetectedObject *)allocator.allocate(sizeof(simple_av_msgs__msg__DetectedObject), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(simple_av_msgs__msg__DetectedObject));
  bool success = simple_av_msgs__msg__DetectedObject__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
simple_av_msgs__msg__DetectedObject__destroy(simple_av_msgs__msg__DetectedObject * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    simple_av_msgs__msg__DetectedObject__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
simple_av_msgs__msg__DetectedObject__Sequence__init(simple_av_msgs__msg__DetectedObject__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__DetectedObject * data = NULL;

  if (size) {
    data = (simple_av_msgs__msg__DetectedObject *)allocator.zero_allocate(size, sizeof(simple_av_msgs__msg__DetectedObject), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = simple_av_msgs__msg__DetectedObject__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        simple_av_msgs__msg__DetectedObject__fini(&data[i - 1]);
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
simple_av_msgs__msg__DetectedObject__Sequence__fini(simple_av_msgs__msg__DetectedObject__Sequence * array)
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
      simple_av_msgs__msg__DetectedObject__fini(&array->data[i]);
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

simple_av_msgs__msg__DetectedObject__Sequence *
simple_av_msgs__msg__DetectedObject__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  simple_av_msgs__msg__DetectedObject__Sequence * array = (simple_av_msgs__msg__DetectedObject__Sequence *)allocator.allocate(sizeof(simple_av_msgs__msg__DetectedObject__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = simple_av_msgs__msg__DetectedObject__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
simple_av_msgs__msg__DetectedObject__Sequence__destroy(simple_av_msgs__msg__DetectedObject__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    simple_av_msgs__msg__DetectedObject__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
simple_av_msgs__msg__DetectedObject__Sequence__are_equal(const simple_av_msgs__msg__DetectedObject__Sequence * lhs, const simple_av_msgs__msg__DetectedObject__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!simple_av_msgs__msg__DetectedObject__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
simple_av_msgs__msg__DetectedObject__Sequence__copy(
  const simple_av_msgs__msg__DetectedObject__Sequence * input,
  simple_av_msgs__msg__DetectedObject__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(simple_av_msgs__msg__DetectedObject);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    simple_av_msgs__msg__DetectedObject * data =
      (simple_av_msgs__msg__DetectedObject *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!simple_av_msgs__msg__DetectedObject__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          simple_av_msgs__msg__DetectedObject__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!simple_av_msgs__msg__DetectedObject__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
