uint64 INVALID=0

# Set station_id to INVALID if the message is directly
# sent from the traffic signal, not from the RSUs
# In such a case, leave station_pose uninitialised
uint64 station_id

# Leave station_pose uninitialised if the message does
# not come from RSUs
geometry_msgs/PoseStamped station_pose

autoware_perception_msgs/TrafficSignalArray traffic_signals
