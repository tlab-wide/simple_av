# System Module

The **System Module** provides supportive functionalities that manage simulation flow and synchronize system-wide parameters for other core modules like Planning and Control.

This module includes two essential nodes:

- `sim_monitor`
- `portal`

These nodes operate behind the scenes to ensure temporal consistency and repeatability within simulation scenarios, especially when running in environments like AWSIM.

---

## 1. sim_monitor

The `sim_monitor` node is responsible for calculating the **simulation clock rate** by subscribing to the `/clock` topic published by AWSIM. It compares the simulated time and the real-world time to estimate the **simulation delay rate** (i.e., how fast or slow the simulation is running compared to real time).

### Why it's important:

- This simulation delay rate is **published periodically** and used in downstream modules such as:
  - `behavior_motion_planning`: For predicting future object positions.
  - `control`: For accurate time-based control computations.

By compensating for the simulation speed difference, these modules can make consistent and real-time-aware decisions.

---

## 2. portal

The `portal` node enables **scenario looping and repetition** by monitoring sudden jumps in vehicle position, which typically occur when the vehicle passes through a **portal** and respawns at a starting point.

### How it works:

- Subscribes to the GNSS pose topic (`/sensing/gnss/pose`).
- Tracks vehicle position over time.
- Detects significant jumps (beyond a threshold), indicating the vehicle has entered a portal.
- Publishes a `portal` message to inform other modules (e.g., Planning) that the scenario has **reset**.

This functionality is particularly useful in testing and evaluation scenarios where repeatability and automated resets are required.

---

## Summary

The System Module ensures that all other modules in the simple-AV stack are:

- **Aware of time distortion** in simulation environments.
- **Synchronized and responsive** to resets in simulation flow (e.g., portal teleportation).

By handling these system-level signals, `sim_monitor` and `portal` provide a stable backbone for accurate simulation, prediction, and testing behavior.
