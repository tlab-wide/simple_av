# Common Package

The `common` package serves as a centralized resource for all shared information across various modules in the simple-AV system. It provides consistent data used by modules such as localization, perception, planning, and control. This package ensures modularity and prevents duplication of configuration and reference files.

The `common` package is structured into three main subfolders:

## 📁 maps

This folder contains the digital map files used by the system. Maps are stored in JSON format and define lanelet structures but in much simpler and lighter way that lanelet standard structor. These maps provide spatial context for localization and planning modules.

[Details about Map structure used by Simple-AV](../../JsonMap/index.md)


## 📁 configs

The `configs` folder holds YAML configuration files that define key parameters and system behavior. These files are loaded by other modules to ensure consistent tuning and logic across the software stack. Below is a summary of the main configuration files:

### **`av_feature.yaml`**  
Controls core AV features:

```bash
# Traffic Light Configuration
traffic_light:
  enable: True   # Enable or disable traffic lights
  use_rsu: True  # Enable or disable RSU for traffic lights
  

# Object Detection Configuration
object_detection:
  enable: True  # Enable or disable object detection
  use_rsu: True # Enable or disable RSU for traffic lights


# Collision Avoidance Configuration
collision_avoidance:
  direct_collision_avoidance: True # Enable or disable direct collision avoidance
  collision_prediction: True       # Enable or disable collision prediction
```



### **`motion_behavior_config.yaml`**  
Specifies the motion behavior and dynamics of the vehicle:

```bash
motion:
  max_turning_angle: 35.0  # Maximum allowable turning angle (degrees)
  
  speed_limits:
    base: 11.0     # Default base speed (m/s)
    turning_speed: 3.0 # Default speed on turns (m/s)

  lookahead:
    coefficient: 1.75    # Scaling factor for lookahead distance
    base: 2.0 # Multiplier based on vehicle speed

behavior:
  safety_distance: 16.0  # Minimum stopping distance behind an object (meters)
  reaction_time_threshold: 4.0  # Time delay before reacting to an event (seconds)
  range_low_pass_gain: 0.90

  on_path_detection_range: # Detection range for Objects on the path
    coefficient: 5.0 # Scaling factor for reaction distance
    base: 25.0        # Base reaction distance (meters)

  prediction_reaction_range: 
    coefficient: 10.0  # Scaling factor for reaction distance
    base: 150.0         # Base reaction distance (meters)

  prediction_detection_range:
    coefficient: 10.0  # Scaling factor for detection radius
    base: 150.0      # Base detection radius (meters)
```

### **`scenario_config.yaml`**  
Provides parameters for simulation scenarios:

- Sets the destination lanelet.
- Allows for repeated testing with a scenario count.
- Defines the vehicle model in use (e.g., `bus`, `lexus`).

```bash
scenario:
  destination: 'lanelet761' # Scenarion 1 lanelet761-- for scenarion 2 enter lanelet1162'
  # destination: 'lanelet177' # Scenarion SHinjuku start from 96
  repeat_count: 50  # Number of times to repeat the scenario for testing
  vehicle_model: 'bus' # Selecting vehicle model based on what model is loaded on AWSIM: Lexus/bus or custom vehicle
```

### **`vehicle_config.yaml`**  
Contains detailed vehicle specifications:

- Defines physical dimensions and dynamic capabilities for supported vehicle models like `lexus` and `bus`.
- Includes speed, acceleration, braking limits, and weights.

```bash
vehicles:
  lexus:
    model: "RX450H"
    dimensions:
      length: 4.8895  # Vehicle length (meters)
      width: 1.895    # Vehicle width (meters)
      height: 1.6     # Vehicle height (meters)
      wheel_base: 2.75 # Distance between front and rear axles (meters)
    weight: 3000  # Vehicle weight (kg)
    performance:
      max_speed: 30.0          # Maximum speed (m/s)
      max_acceleration: 3.8     # Maximum acceleration (m/s²)
      max_braking_acceleration: -6.0 # Maximum braking acceleration (m/s²)

  bus:
    model: "TierIV"
    dimensions:
      length: 10.3   # Vehicle length (meters)
      width: 2.9     # Vehicle width (meters)
      height: 3.2    # Vehicle height (meters)
      wheel_base: 4.8 # Distance between front and rear axles (meters)
      front_overhang: 2.3 # Distance from front axle to vehicle front (meters)
      rear_overhang: 3.2  # Distance from rear axle to vehicle back (meters)
    weight: 10000  # Vehicle weight (kg)
    performance:
      max_speed: 20.0          # Maximum speed (m/s)
      max_acceleration: 1.4     # Maximum acceleration (m/s²)
      max_braking_acceleration: -2.6 # Maximum braking acceleration (m/s²)

```

## 📁 zones

The `zones` folder contains metadata about specific geographic zones used within the system. One key file here is: **`intersection_profiles.yaml`**  

Describes intersection areas with:

  - A `name` for each intersection.
  - A `reference_point` (x, y coordinates) marking the center of the intersection.
  - A `threshold` distance that defines the proximity boundary around each reference point.

```bash
  intersections:
  intersection_1:
    name: "intersection_1"
    reference_point: 
      x: 4250.0
      y: 73455.0
    threshold: 40.0
```

These profiles are utilized in the `intersection_detection` node to determine whether the vehicle is approaching, inside, or exiting an intersection area.

---

By organizing shared data in the `common` package, all modules operate with a consistent and centralized set of information, which simplifies development and improves maintainability.
