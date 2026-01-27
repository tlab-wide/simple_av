// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from autoware_perception_msgs:msg/TrafficLightGroup.idl
// generated code does not contain a copyright notice
#include "autoware_perception_msgs/msg/detail/traffic_light_group__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `elements`
#include "autoware_perception_msgs/msg/detail/traffic_light_element__functions.h"
// Member `predictions`
#include "autoware_perception_msgs/msg/detail/predicted_traffic_light_state__functions.h"

bool
autoware_perception_msgs__msg__TrafficLightGroup__init(autoware_perception_msgs__msg__TrafficLightGroup * msg)
{
  if (!msg) {
    return false;
  }
  // traffic_light_group_id
  // elements
  if (!autoware_perception_msgs__msg__TrafficLightElement__Sequence__init(&msg->elements, 0)) {
    autoware_perception_msgs__msg__TrafficLightGroup__fini(msg);
    return false;
  }
  // predictions
  if (!autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__init(&msg->predictions, 0)) {
    autoware_perception_msgs__msg__TrafficLightGroup__fini(msg);
    return false;
  }
  return true;
}

void
autoware_perception_msgs__msg__TrafficLightGroup__fini(autoware_perception_msgs__msg__TrafficLightGroup * msg)
{
  if (!msg) {
    return;
  }
  // traffic_light_group_id
  // elements
  autoware_perception_msgs__msg__TrafficLightElement__Sequence__fini(&msg->elements);
  // predictions
  autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__fini(&msg->predictions);
}

bool
autoware_perception_msgs__msg__TrafficLightGroup__are_equal(const autoware_perception_msgs__msg__TrafficLightGroup * lhs, const autoware_perception_msgs__msg__TrafficLightGroup * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // traffic_light_group_id
  if (lhs->traffic_light_group_id != rhs->traffic_light_group_id) {
    return false;
  }
  // elements
  if (!autoware_perception_msgs__msg__TrafficLightElement__Sequence__are_equal(
      &(lhs->elements), &(rhs->elements)))
  {
    return false;
  }
  // predictions
  if (!autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__are_equal(
      &(lhs->predictions), &(rhs->predictions)))
  {
    return false;
  }
  return true;
}

bool
autoware_perception_msgs__msg__TrafficLightGroup__copy(
  const autoware_perception_msgs__msg__TrafficLightGroup * input,
  autoware_perception_msgs__msg__TrafficLightGroup * output)
{
  if (!input || !output) {
    return false;
  }
  // traffic_light_group_id
  output->traffic_light_group_id = input->traffic_light_group_id;
  // elements
  if (!autoware_perception_msgs__msg__TrafficLightElement__Sequence__copy(
      &(input->elements), &(output->elements)))
  {
    return false;
  }
  // predictions
  if (!autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__copy(
      &(input->predictions), &(output->predictions)))
  {
    return false;
  }
  return true;
}

autoware_perception_msgs__msg__TrafficLightGroup *
autoware_perception_msgs__msg__TrafficLightGroup__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_perception_msgs__msg__TrafficLightGroup * msg = (autoware_perception_msgs__msg__TrafficLightGroup *)allocator.allocate(sizeof(autoware_perception_msgs__msg__TrafficLightGroup), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(autoware_perception_msgs__msg__TrafficLightGroup));
  bool success = autoware_perception_msgs__msg__TrafficLightGroup__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
autoware_perception_msgs__msg__TrafficLightGroup__destroy(autoware_perception_msgs__msg__TrafficLightGroup * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    autoware_perception_msgs__msg__TrafficLightGroup__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
autoware_perception_msgs__msg__TrafficLightGroup__Sequence__init(autoware_perception_msgs__msg__TrafficLightGroup__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_perception_msgs__msg__TrafficLightGroup * data = NULL;

  if (size) {
    data = (autoware_perception_msgs__msg__TrafficLightGroup *)allocator.zero_allocate(size, sizeof(autoware_perception_msgs__msg__TrafficLightGroup), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = autoware_perception_msgs__msg__TrafficLightGroup__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        autoware_perception_msgs__msg__TrafficLightGroup__fini(&data[i - 1]);
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
autoware_perception_msgs__msg__TrafficLightGroup__Sequence__fini(autoware_perception_msgs__msg__TrafficLightGroup__Sequence * array)
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
      autoware_perception_msgs__msg__TrafficLightGroup__fini(&array->data[i]);
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

autoware_perception_msgs__msg__TrafficLightGroup__Sequence *
autoware_perception_msgs__msg__TrafficLightGroup__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_perception_msgs__msg__TrafficLightGroup__Sequence * array = (autoware_perception_msgs__msg__TrafficLightGroup__Sequence *)allocator.allocate(sizeof(autoware_perception_msgs__msg__TrafficLightGroup__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = autoware_perception_msgs__msg__TrafficLightGroup__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
autoware_perception_msgs__msg__TrafficLightGroup__Sequence__destroy(autoware_perception_msgs__msg__TrafficLightGroup__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    autoware_perception_msgs__msg__TrafficLightGroup__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
autoware_perception_msgs__msg__TrafficLightGroup__Sequence__are_equal(const autoware_perception_msgs__msg__TrafficLightGroup__Sequence * lhs, const autoware_perception_msgs__msg__TrafficLightGroup__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!autoware_perception_msgs__msg__TrafficLightGroup__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
autoware_perception_msgs__msg__TrafficLightGroup__Sequence__copy(
  const autoware_perception_msgs__msg__TrafficLightGroup__Sequence * input,
  autoware_perception_msgs__msg__TrafficLightGroup__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(autoware_perception_msgs__msg__TrafficLightGroup);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    autoware_perception_msgs__msg__TrafficLightGroup * data =
      (autoware_perception_msgs__msg__TrafficLightGroup *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!autoware_perception_msgs__msg__TrafficLightGroup__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          autoware_perception_msgs__msg__TrafficLightGroup__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!autoware_perception_msgs__msg__TrafficLightGroup__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
