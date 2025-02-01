import rclpy
from rclpy.node import Node
from rosgraph_msgs.msg import Clock
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy
from simple_av_msgs.msg import SimFrequency

class ClockRateCalculator(Node):
    def __init__(self):
        super().__init__('clock_rate_calculator')
        
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
        
        # Variables to store the last timestamp and rate
        self.last_time = None
        self.rate_hz = 0.0
    
    def clock_callback(self, msg):
        current_time = self.get_timestamp_in_seconds(msg)

        if self.last_time is not None:
            time_diff = current_time - self.last_time
            if time_diff > 0:
                self.rate_hz = 1.0 / time_diff
                self.get_logger().info(f'Clock rate: {self.rate_hz:.2f} Hz')
        
        self.last_time = current_time


    def clock_callback(self, msg):
        # Get the current time from the message
        current_time = self.get_timestamp_in_seconds(msg)
        print("current time: ", current_time)

        if self.last_time is not None:
            # Calculate the time difference between messages
            time_diff = current_time - self.last_time
            print("time diff: ", time_diff)
            
            # Calculate the rate (Hz) as the inverse of the time difference
            if time_diff > 0:
                self.rate_hz = 1.0 / time_diff
                self.get_logger().info(f'Clock rate: {self.rate_hz} Hz')
                freq_msg = SimFrequency()
                freq_msg.frequency = float(self.rate_hz)
                self.publisher.publish(freq_msg)
        
        # Update the last time
        self.last_time = current_time

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