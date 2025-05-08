# Quick Start Demo

## 1. Simple AV Project

### Repository Structure

This repository contains the following key directories:

| Directory                  | Description                                                                                                             |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------|
| **simple_av/**             | Contains the main launch file to run the entire Simple-AV system.                                                         |
| **V2X_messages/**          | Includes the custom ROS message definitions that interface with the AWSIM environment.                                     |
| **simple_av_msgs/**        | Defines internal message types used for communication between the Simple-AV nodes.                                         |
| **common/**                | Contains shared data such as maps, configurations, and zones that are utilized by multiple modules.                        |
| **system/**                | Includes utility nodes like `portal` for scenario repetition and `sim_monitor` for monitoring simulation delay.            |
| **control/**               | Contains the control node responsible for executing vehicle maneuvers.                                                    |
| **localization/**          | Contains nodes for determining the vehicle's position, including `localization` and `intersection_detector`.                |
| **planning/**              | Includes planning nodes such as `mission_planning`, `behavior_path_planning`, and `behavior_motion_planning`.               |
| **perception/**            | Contains perception nodes, including `traffic_light_handler` and `object_detection_handler`.                               |

### Getting Started

To use this project, you'll need to set up a ROS 2 workspace and clone the necessary packages.

#### Step 0: Setup the Environment.
Refer to the [system setup page](../../Simple-AV/SystemSetup/index.md) for detailed instructions.

#### Step 1: Create a ROS Workspace
First, create a new ROS workspace:

```bash
mkdir -p ~/ros_ws/src
```

#### Step 2: Clone the Repository
Next, clone this repository into the src directory of your workspace:

```bash
cd ~/ros_ws/src
git clone https://github.com/hoosh-ir/simple_av.git
```

#### Step 3: Build the Workspace
After cloning the repository, build the workspace using colcon:
```bash
cd ~/ros_ws/
colcon build
```

The workspace should look like this after running `colcon build`:
```bash
ros_ws/
├── build/
├── install/
├── log/
└── src/
    ├── docs/
    ├── mkdocs.yml
    ├── README.md
    └── src/
      ├── V2X_messages/
      ├── simple_av_msgs/
      ├── common/
      ├── system/
      ├── control/
      ├── localization/
      ├── planning/
      ├── perception/
      └── simple_av/
          ├── package.xml
          ├── resource/
          ├── setup.cfg
          ├── setup.py
          └── launch/
              └── launch_all.py
```

#### Step 4: Source the Workspace
Finally, source the workspace to make the ROS packages available:

```bash
source ~/ros_ws/install/setup.bash
```

#### Step 5: Running the Project
You can run the project by either running the launch file or by manually starting each node in sequence.

Run the launch file:
```bash
ros2 launch simple_av launch_all.py
```

Or, run the nodes manually in the following order:

```bash
ros2 run localization localization
ros2 run localization intersection_detector
ros2 run system portal
ros2 run system sim_monitor
ros2 run perception traffic_light_handler
ros2 run perception object_detection_handler
ros2 run planning mission_planning
ros2 run planning behavior_path_planning
ros2 run planning behavior_motion_planning
ros2 run control control
```

---

## 2. Running Simple-AV with AWSIM

Simple-AV is designed to work seamlessly alongside AWSIM. AWSIM acts as the simulation environment, providing sensor data and scene information. Simple-AV processes this data to perform localization, perception, planning, and control tasks. The computed control commands are then sent back to AWSIM, which moves the vehicle accordingly within the simulated environment.

### AWSIM Integration

AWSIM serves as the primary source of sensory input for Simple-AV. The data, such as GNSS positions, detected objects, and traffic signal states, is received from AWSIM. Simple-AV processes this data and generates the necessary control commands (throttle, brake, steering), which are sent back to AWSIM to move the vehicle in the scene.

### V2X_E2E Project

We have developed another open-source project named **V2X_E2E**, which integrates with Simple-AV to extend the capabilities of AWSIM. For more information about how to use our latest version and how to modify the scenes, please visit [V2X_E2E Project Page]( ).

If you do not wish to modify AWSIM scenes using Unity, you can use the pre-built versions of AWSIM provided. These versions come with pre-configured scenes and vehicle models (Lexus and Bus) for straightforward testing.

The Scenes below are built for Windows environment. stay tuned for the ubuntu builds.

- [AWSIM Built Version with Lexus](https://drive.google.com/drive/folders/1GCXG6S2MeOMjNjEbMUlYO2JOUidEjU7R?usp=drive_link)  
- [AWSIM Built Version with Bus](https://drive.google.com/drive/folders/10Y8swA4Zfuh_U34EDGDr4i4As6Yidrfr?usp=drive_link)

