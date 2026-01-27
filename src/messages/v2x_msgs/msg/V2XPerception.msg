uint64 station_id
uint64 sensor_type
geometry_msgs/PoseStamped station_pose

# The reason we use PredictedObjects message type is that we can put the object Id, 
# and we can also put predicted path from AWSIM side to the mesage 

autoware_perception_msgs/PredictedObjects predicted_objects
