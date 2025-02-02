import rclpy
from rclpy.node import Node
from rosgraph_msgs.msg import Clock
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from simple_av_msgs.msg import SimFrequency
from collections import deque
import numpy as np
import time
from rclpy.parameter import Parameter

class ClockRateCalculator(Node):
    def __init__(self):
        super().__init__('clock_rate_calculator')

        if not self.has_parameter('use_sim_time'):
            self.declare_parameter('use_sim_time', True)
        self.set_parameters([Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        
        # Define the QoS profile to match the publisher
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,  # Match reliability
            history=QoSHistoryPolicy.KEEP_LAST,            # Match history
            depth=1,                                       # Match depth
            durability=QoSDurabilityPolicy.VOLATILE        # Match durability
        )
        
        # Subscribe to the /clock topic with the custom QoS profile
        self.subscription = self.create_subscription(
            Clock,  # Message type for /clock
            '/clock',  # Topic name
            self.clock_callback,  # Callback function
            qos_profile  # Use the custom QoS profile
        )
        self.publisher = self.create_publisher(SimFrequency, 'simple_av/sim_monitor', 10)
        
        # Buffer to store recent timestamps (window size similar to ros2 topic hz)
        self.samples = deque(maxlen=1000)  # Rolling buffer for timestamps
    
    def clock_callback(self, msg):
        current_time = self.get_timestamp_in_seconds(msg)
        self.samples.append(current_time)
        print("-----start------")
        print(current_time)
        t1 = self.get_clock().now().nanoseconds/ 1e9
        print(t1)


        return

        if len(self.samples) > 1:
            time_diffs = np.diff(self.samples)
            
            # Compute statistics like ros2 topic hz
            mean_interval = np.mean(time_diffs)
            min_diff = np.min(time_diffs)
            max_diff = np.max(time_diffs)
            std_dev = np.std(time_diffs)

            # Calculate frequency as 1 / mean interval
            if mean_interval > 0:
                self.rate_hz = 1.0 / mean_interval

                # Log results
                self.get_logger().info(
                    f'\nAverage rate: {self.rate_hz:.3f} Hz\n'
                    f'min: {min_diff:.3f}s max: {max_diff:.3f}s std dev: {std_dev:.5f}s window: {len(self.samples)}'
                )

                # Publish frequency message
                freq_msg = SimFrequency()
                freq_msg.frequency = float(self.rate_hz)
                self.publisher.publish(freq_msg)

    def get_timestamp_in_seconds(self, msg):
        # Convert the Clock message (seconds and nanoseconds) to a single float (seconds)
        return msg.clock.sec + msg.clock.nanosec / 1e9

def main(args=None):
    rclpy.init(args=args)
    
    # Create the node
    clock_rate_calculator = ClockRateCalculator()
    
    # Spin the node to process callbacks
    rclpy.spin(clock_rate_calculator)
    
    # Clean up
    clock_rate_calculator.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
