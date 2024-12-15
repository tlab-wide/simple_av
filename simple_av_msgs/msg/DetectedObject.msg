# Detected object label
int32 label

# relative Position of the detected object
geometry_msgs/Point relative_position

# relative distance of the detected object
geometry_msgs/Point relative_distance

# Orientation of the detected object
geometry_msgs/Quaternion orientation

# Shape of the detected object (dimensions: x, y, z)
geometry_msgs/Vector3 shape

# relative distance of the vehicle with the detected object
float64 distance