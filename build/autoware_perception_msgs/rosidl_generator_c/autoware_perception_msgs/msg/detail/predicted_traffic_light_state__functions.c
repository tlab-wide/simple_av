// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from autoware_perception_msgs:msg/PredictedTrafficLightState.idl
// generated code does not contain a copyright notice
#include "autoware_perception_msgs/msg/detail/predicted_traffic_light_state__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `predicted_stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"
// Member `simultaneous_elements`
#include "autoware_perception_msgs/msg/detail/traffic_light_element__functions.h"
// Member `information_source`
#include "rosidl_runtime_c/string_functions.h"

bool
autoware_perception_msgs__msg__PredictedTrafficLightState__init(autoware_perception_msgs__msg__PredictedTrafficLightState * msg)
{
  if (!msg) {
    return false;
  }
  // predicted_stamp
  if (!builtin_interfaces__msg__Time__init(&msg->predicted_stamp)) {
    autoware_perception_msgs__msg__PredictedTrafficLightState__fini(msg);
    return false;
  }
  // simultaneous_elements
  if (!autoware_perception_msgs__msg__TrafficLightElement__Sequence__init(&msg->simultaneous_elements, 0)) {
    autoware_perception_msgs__msg__PredictedTrafficLightState__fini(msg);
    return false;
  }
  // reliability
  // information_source
  if (!rosidl_runtime_c__String__init(&msg->information_source)) {
    autoware_perception_msgs__msg__PredictedTrafficLightState__fini(msg);
    return false;
  }
  return true;
}

void
autoware_perception_msgs__msg__PredictedTrafficLightState__fini(autoware_perception_msgs__msg__PredictedTrafficLightState * msg)
{
  if (!msg) {
    return;
  }
  // predicted_stamp
  builtin_interfaces__msg__Time__fini(&msg->predicted_stamp);
  // simultaneous_elements
  autoware_perception_msgs__msg__TrafficLightElement__Sequence__fini(&msg->simultaneous_elements);
  // reliability
  // information_source
  rosidl_runtime_c__String__fini(&msg->information_source);
}

bool
autoware_perception_msgs__msg__PredictedTrafficLightState__are_equal(const autoware_perception_msgs__msg__PredictedTrafficLightState * lhs, const autoware_perception_msgs__msg__PredictedTrafficLightState * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // predicted_stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->predicted_stamp), &(rhs->predicted_stamp)))
  {
    return false;
  }
  // simultaneous_elements
  if (!autoware_perception_msgs__msg__TrafficLightElement__Sequence__are_equal(
      &(lhs->simultaneous_elements), &(rhs->simultaneous_elements)))
  {
    return false;
  }
  // reliability
  if (lhs->reliability != rhs->reliability) {
    return false;
  }
  // information_source
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->information_source), &(rhs->information_source)))
  {
    return false;
  }
  return true;
}

bool
autoware_perception_msgs__msg__PredictedTrafficLightState__copy(
  const autoware_perception_msgs__msg__PredictedTrafficLightState * input,
  autoware_perception_msgs__msg__PredictedTrafficLightState * output)
{
  if (!input || !output) {
    return false;
  }
  // predicted_stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->predicted_stamp), &(output->predicted_stamp)))
  {
    return false;
  }
  // simultaneous_elements
  if (!autoware_perception_msgs__msg__TrafficLightElement__Sequence__copy(
      &(input->simultaneous_elements), &(output->simultaneous_elements)))
  {
    return false;
  }
  // reliability
  output->reliability = input->reliability;
  // information_source
  if (!rosidl_runtime_c__String__copy(
      &(input->information_source), &(output->information_source)))
  {
    return false;
  }
  return true;
}

autoware_perception_msgs__msg__PredictedTrafficLightState *
autoware_perception_msgs__msg__PredictedTrafficLightState__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_perception_msgs__msg__PredictedTrafficLightState * msg = (autoware_perception_msgs__msg__PredictedTrafficLightState *)allocator.allocate(sizeof(autoware_perception_msgs__msg__PredictedTrafficLightState), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(autoware_perception_msgs__msg__PredictedTrafficLightState));
  bool success = autoware_perception_msgs__msg__PredictedTrafficLightState__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
autoware_perception_msgs__msg__PredictedTrafficLightState__destroy(autoware_perception_msgs__msg__PredictedTrafficLightState * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    autoware_perception_msgs__msg__PredictedTrafficLightState__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__init(autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_perception_msgs__msg__PredictedTrafficLightState * data = NULL;

  if (size) {
    data = (autoware_perception_msgs__msg__PredictedTrafficLightState *)allocator.zero_allocate(size, sizeof(autoware_perception_msgs__msg__PredictedTrafficLightState), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = autoware_perception_msgs__msg__PredictedTrafficLightState__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        autoware_perception_msgs__msg__PredictedTrafficLightState__fini(&data[i - 1]);
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
autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__fini(autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence * array)
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
      autoware_perception_msgs__msg__PredictedTrafficLightState__fini(&array->data[i]);
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

autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence *
autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence * array = (autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence *)allocator.allocate(sizeof(autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__destroy(autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__are_equal(const autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence * lhs, const autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!autoware_perception_msgs__msg__PredictedTrafficLightState__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence__copy(
  const autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence * input,
  autoware_perception_msgs__msg__PredictedTrafficLightState__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(autoware_perception_msgs__msg__PredictedTrafficLightState);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    autoware_perception_msgs__msg__PredictedTrafficLightState * data =
      (autoware_perception_msgs__msg__PredictedTrafficLightState *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!autoware_perception_msgs__msg__PredictedTrafficLightState__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          autoware_perception_msgs__msg__PredictedTrafficLightState__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!autoware_perception_msgs__msg__PredictedTrafficLightState__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
