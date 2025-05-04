# Localization Module

The Localization module in simple-AV is designed to accurately determine the position and orientation of the autonomous vehicle within its environment using GNSS/pose data. This module is crucial for ensuring that the vehicle can navigate safely and effectively, as it provides the foundational data needed for all subsequent decision-making processes, such as perception, planning, and control.

## Overview

Localization is achieved by utilizing GNSS/pose data to determine the vehicle's position within a predefined map. This map is stored in a JSON file, which includes detailed information about the city's lanelets, their connections, waypoints, and traffic light locations. The Localization module processes this data to identify the vehicle's current lane and the closest waypoint within that lane.

## Key Components

- **GNSS/Pose Data:** Provides the vehicle's current coordinates (x, y, z). This data is used to determine the vehicle's position relative to the predefined map.

- **JSON Map:** Contains all lanelets of the city, including their next, previous, and adjacent lanes. Each lanelet consists of waypoints and traffic light information, providing a comprehensive representation of the driving environment.

## Nodes

1. **Localization:** Used for determining the current lane and waypoint of the vehicle
2. **intersection detector:** Used for intersection awarenes

## Functionality

1. **Localization:** The Localization Node performs several critical functions to ensure accurate and reliable vehicle positioning:

    - **Global Localization:** At the beginning of the process, the global localization component compares the GNSS/pose data to all the waypoints in each lanelet. This step determines the currently occupied lane and is computationally intensive, so it is only performed initially to establish the vehicle's starting position.

    - **Local Localization:** Once the vehicle's initial position is determined, the local localization component takes over. It creates a search area based on the current lane to limit the computational load. This localized search ensures that the process is efficient and can run in real-time without excessive computational demands.

    - **Lane and Waypoint Determination:** The module continuously checks if the vehicle is within the current lane and identifies which waypoint is closest to the vehicle. This helps in maintaining accurate localization and provides essential data for navigation.

2. **intersection detector:** The `intersection_detector` node analyzes the vehicle's position relative to known intersections on the map. It determines:
    - Whether the vehicle is currently approaching, inside or exiting an intersection.

3. **Topic Creation:**  
    - `simple_av/localization/location`: Includes the current lane, closest waypoint, and distance to the waypoint.  
    - `simple_av/localization/intersection_status`: Created by the `intersection_detector` node, this topic publishes detailed information about nearby intersections and the vehicle's relation to them.



## Integration

The Localization module is tightly integrated with several other components of the simple-AV software stack:

**Planning Module:**  

- Relies on precise localization to generate safe and feasible trajectories for the vehicle to follow.

**Perception Module:**

- The `objectDetectionHandler` and `trafficLightHandler` nodes subscribe to the `simple_av/localization/intersection_status` topic published by the `intersection_detector` node.
- This intersection-aware data enables perception nodes to adjust their behavior depending on the vehicle’s current intersection context.

**Object Detection Usage:**

- The vehicle receives object detections from its onboard sensors via the `/OBU/sensing` topic.
- Additionally, simple-AV leverages V2X data from Road Side Units (RSUs) at intersections. This data is received on topics of the form `/v2x/predictedObjects<n>`, where `<n>` is the intersection's assigned number.
- The `objectDetectionHandler` uses the output of the `intersection_detector` node to determine which intersection the vehicle is near, and thus which RSU topic to subscribe to for relevant external object data.

**Traffic Light Handling:**

- Traffic signal states are broadcast on topics like `/v2x/traffic_Signals/intersection_1`, with each topic corresponding to a specific intersection.
- The `trafficLightHandler` node uses the `intersection_detector`'s output to identify the relevant intersection and select the appropriate traffic signal topic to monitor.

This intelligent use of intersection context allows perception nodes to operate with greater specificity and reliability, ensuring that the most relevant external data is processed depending on the vehicle's current location within the environment.
