# Intersection Traffic Signal Synchronization with RSU

One of the practical features enabled by integrating **RSUs (Road Side Units)** at intersections in simple-AV is the ability to share traffic signal states across multiple lanes within the intersection. This feature is especially beneficial in scenarios where traffic lights at different sides of an intersection are synchronized with a small delay, such as in **T-junctions**.

## Problem Statement

In a standard autonomous vehicle setup, the vehicle is only aware of the state of the traffic light directly in front of it. This limited awareness can lead to inefficient decision-making, particularly at intersections where the traffic light state on the opposite side is slightly delayed but synchronized.

### Example Scenario: T-Junction

Imagine a **T-junction** (illustrated below), where:
- On one side of the junction, a vehicle is positioned in a lane that allows a **right turn**.
- On the opposite side, a vehicle is positioned in a lane that allows a **left turn** onto the same road.

The traffic signals on both sides of the junction are synchronized with a slight delay (e.g., **8 seconds**). When the vehicle on one side gets a green light to turn right, the vehicle on the opposite side still has a red light for a few seconds before it also turns green.

<video width="1920" controls autoplay muted loop>
    <source src="intersectionTrafficState.mp4" type="video/mp4">
</video>

### Issue

If the vehicle on one side only knows its own traffic light state:
- The vehicle detects an approaching vehicle from the opposite side.
- Even though the opposing vehicle's traffic light is red, the vehicle hesitates, predicting a potential collision.
- This hesitation wastes valuable time and may cause the vehicle to miss the opportunity to move before the light turns red again.

## RSU-Enhanced Solution

With RSU integration in simple-AV, we publish the traffic signal states of **all relevant lanes at the intersection**. This allows the vehicle to:
- Be aware of the **state of opposite traffic lights**.
- Accurately **predict when vehicles from the opposite side will stop**, rather than assuming they are continuously moving.
- Make a **confident decision to proceed** without unnecessary hesitation.

## Real-World Benefit

By integrating RSU data for traffic signal synchronization, we eliminate unnecessary hesitation and improve **intersection efficiency**. Vehicles can make more **timely and accurate decisions**, reducing the risk of missing the green light due to over-cautious behavior.

## Visual Example: T-Junction

Below is a visual representation of a typical **T-junction** where RSU data is critical for efficient decision-making. First video below demonstrates the Ego vehicle's performance without awareness of the opposite traffic signal state, while the seconds video shows its performance when this awareness is enabled.

<video width="1920" controls autoplay muted loop>
    <source src="g2.mp4" type="video/mp4">
</video>

<video width="1920" controls autoplay muted loop>
    <source src="g1.mp4" type="video/mp4">
</video>


