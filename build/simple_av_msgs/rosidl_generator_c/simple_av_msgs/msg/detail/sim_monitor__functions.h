// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from simple_av_msgs:msg/SimMonitor.idl
// generated code does not contain a copyright notice

#ifndef SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__FUNCTIONS_H_
#define SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "simple_av_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "simple_av_msgs/msg/detail/sim_monitor__struct.h"

/// Initialize msg/SimMonitor message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * simple_av_msgs__msg__SimMonitor
 * )) before or use
 * simple_av_msgs__msg__SimMonitor__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
bool
simple_av_msgs__msg__SimMonitor__init(simple_av_msgs__msg__SimMonitor * msg);

/// Finalize msg/SimMonitor message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
void
simple_av_msgs__msg__SimMonitor__fini(simple_av_msgs__msg__SimMonitor * msg);

/// Create msg/SimMonitor message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * simple_av_msgs__msg__SimMonitor__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
simple_av_msgs__msg__SimMonitor *
simple_av_msgs__msg__SimMonitor__create();

/// Destroy msg/SimMonitor message.
/**
 * It calls
 * simple_av_msgs__msg__SimMonitor__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
void
simple_av_msgs__msg__SimMonitor__destroy(simple_av_msgs__msg__SimMonitor * msg);

/// Check for msg/SimMonitor message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
bool
simple_av_msgs__msg__SimMonitor__are_equal(const simple_av_msgs__msg__SimMonitor * lhs, const simple_av_msgs__msg__SimMonitor * rhs);

/// Copy a msg/SimMonitor message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
bool
simple_av_msgs__msg__SimMonitor__copy(
  const simple_av_msgs__msg__SimMonitor * input,
  simple_av_msgs__msg__SimMonitor * output);

/// Initialize array of msg/SimMonitor messages.
/**
 * It allocates the memory for the number of elements and calls
 * simple_av_msgs__msg__SimMonitor__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
bool
simple_av_msgs__msg__SimMonitor__Sequence__init(simple_av_msgs__msg__SimMonitor__Sequence * array, size_t size);

/// Finalize array of msg/SimMonitor messages.
/**
 * It calls
 * simple_av_msgs__msg__SimMonitor__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
void
simple_av_msgs__msg__SimMonitor__Sequence__fini(simple_av_msgs__msg__SimMonitor__Sequence * array);

/// Create array of msg/SimMonitor messages.
/**
 * It allocates the memory for the array and calls
 * simple_av_msgs__msg__SimMonitor__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
simple_av_msgs__msg__SimMonitor__Sequence *
simple_av_msgs__msg__SimMonitor__Sequence__create(size_t size);

/// Destroy array of msg/SimMonitor messages.
/**
 * It calls
 * simple_av_msgs__msg__SimMonitor__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
void
simple_av_msgs__msg__SimMonitor__Sequence__destroy(simple_av_msgs__msg__SimMonitor__Sequence * array);

/// Check for msg/SimMonitor message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
bool
simple_av_msgs__msg__SimMonitor__Sequence__are_equal(const simple_av_msgs__msg__SimMonitor__Sequence * lhs, const simple_av_msgs__msg__SimMonitor__Sequence * rhs);

/// Copy an array of msg/SimMonitor messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_simple_av_msgs
bool
simple_av_msgs__msg__SimMonitor__Sequence__copy(
  const simple_av_msgs__msg__SimMonitor__Sequence * input,
  simple_av_msgs__msg__SimMonitor__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // SIMPLE_AV_MSGS__MSG__DETAIL__SIM_MONITOR__FUNCTIONS_H_
