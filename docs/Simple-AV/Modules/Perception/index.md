# Perception Module

The **Perception Module** is responsible for interpreting the surrounding environment using both onboard and infrastructure-based sensors. It detects dynamic and static objects, tracks traffic signal states, and enables the autonomous system to perceive and respond to its surroundings accurately.

This module primarily includes two critical nodes:

- `objectDetectionHandler`
- `trafficLightHandler`

It works in conjunction with the **Localization** module and uses data from both the vehicle sensors and RSUs (Roadside Units) placed at intersections.

---

## 1. objectDetectionHandler

This node is responsible for fusing and managing detected object data from various sources:

- **Onboard Sensors**: Object detections are received on the `/OBU/sensing` topic from sensors mounted on the vehicle.
- **RSU Sensors**: Detected objects from intersection-mounted RSUs are received on topics of the form `/v2x/predictedObjects*n`, where `n` is the intersection number.

The `objectDetectionHandler` uses the `intersection_status` topic published by the **Localization Module** to determine which intersection the vehicle is approaching. This allows it to select the relevant RSU topic and fuse the correct data into the perception pipeline.

This fused data is then used by the planning modules, particularly the `behavior_motion_planning` node, for decision-making and collision avoidance.

---

## 2. trafficLightHandler

This node handles the perception of traffic signal states and is vital for legal and safe navigation through intersections.

- Traffic light data is received from RSUs on topics of the form:
  - `/v2x/traffic_Signals/intersection_n`, where `n` corresponds to the intersection number.

Similar to `objectDetectionHandler`, this node also listens to `simple_av/localization/intersection_status` to identify the current intersection and determine which topic it should subscribe to for traffic signal data.

It then parses and publishes the status of traffic lights (e.g., red, yellow, green), which is consumed by the `behavior_motion_planning` node to determine whether the vehicle should stop or proceed.

---

## Integration with Localization

Both nodes in the Perception Module rely on the intersection status published by the **Localization Module** (`simple_av/localization/intersection_status`). This tight integration ensures that perception components use the right context when handling RSU-based data, especially at intersections.

---

## Summary

The Perception Module plays a vital role in situational awareness for the autonomous vehicle. It achieves this by:

- Aggregating object detections from onboard and infrastructure sensors.
- Providing real-time traffic signal status.
- Leveraging localization to focus on relevant intersection-specific data.

This information feeds directly into the Planning Module, enabling accurate, safe, and context-aware behavior planning.
