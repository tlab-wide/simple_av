import rclpy
from rclpy.node import Node
from builtin_interfaces.msg import Time
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy, QoSHistoryPolicy

class ClockRateCalculator(Node):
    def __init__(self):
        super().__init__('clock_rate_calculator')
        
        # Define the QoS profile to match the publisher
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,  # Match reliability
            durability=QoSDurabilityPolicy.VOLATILE,    # Match durability
            history=QoSHistoryPolicy.KEEP_LAST,         # Match history
            depth=10                                    # Match depth
        )
        
        # Subscribe to the /clock topic with the custom QoS profile
        self.subscription = self.create_subscription(
            Time,  # Message type for /clock
            '/clock',  # Topic name
            self.clock_callback,  # Callback function
            qos_profile  # Use the custom QoS profile
        )
        
        # Variables to store the last timestamp and rate
        self.last_time = None
        self.rate_hz = 0.0

    def clock_callback(self, msg):
        # Get the current time from the message
        current_time = self.get_timestamp_in_seconds(msg)

        if self.last_time is not None:
            # Calculate the time difference between messages
            time_diff = current_time - self.last_time
            
            # Calculate the rate (Hz) as the inverse of the time difference
            if time_diff > 0:
                self.rate_hz = 1.0 / time_diff
                self.get_logger().info(f'Clock rate: {self.rate_hz:.2f} Hz')
        
        # Update the last time
        self.last_time = current_time

    def get_timestamp_in_seconds(self, msg):
        # Convert the Time message (seconds and nanoseconds) to a single float (seconds)
        return msg.sec + msg.nanosec / 1e9

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