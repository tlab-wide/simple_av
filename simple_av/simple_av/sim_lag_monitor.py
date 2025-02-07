import rclpy
from rclpy.node import Node
from rosgraph_msgs.msg import Clock
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from simple_av_msgs.msg import SimMonitor
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
        self.publisher = self.create_publisher(SimMonitor, 'simple_av/sim_monitor', 10)
        
        self.last_system_t = 0
        self.last_sim_t = 0
        self.last_t1 = 0

        self.system_snap_shot = 0
        self.sim_snap_shot = 0
        self.has_seccond_passed = True

        self.lag = 1.0

    
    def clock_callback(self, msg):
        sim_time = self.get_timestamp_in_seconds(msg)
        system_time = time.time()
        t1 = self.get_clock().now().nanoseconds/ 1e9

        if self.has_seccond_passed:
            self.system_snap_shot = system_time
            self.sim_snap_shot = sim_time
            self.has_seccond_passed = False
        if system_time - self.system_snap_shot >= 1.0 and not self.has_seccond_passed:
            # print(f"{system_time - self.system_snap_shot} seccond has passed in system")
            # print(f"{sim_time - self.sim_snap_shot} secconds has passed in awsim")
            self.has_seccond_passed = True
            self.lag = (sim_time - self.sim_snap_shot)/(system_time - self.system_snap_shot)
            if self.lag > 1: 
                self.lag = 1.0
            print(f"lag: {self.lag}")

        '''
        print("-----------")
        print(f"awsim clock: {sim_time} time passed = {sim_time - self.last_sim_t}")
        print(f"system time: {system_time} time passed = {system_time - self.last_system_t}")
        print(f"t1         : {t1} time passed = {t1 - self.last_t1}")
        print(f"awsim/system time {(t1 - self.last_t1)/(system_time - self.last_system_t)}")
        print(f"system/awsim time {(system_time - self.last_system_t)/(t1 - self.last_t1)}")
        self.last_system_t = system_time
        self.last_sim_t = sim_time
        self.last_t1 = t1
        '''

        sim_monitor = SimMonitor()
        sim_monitor.system_time = system_time
        sim_monitor.sim_time = sim_time
        sim_monitor.lag = self.lag
        self.publisher.publish(sim_monitor)

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
