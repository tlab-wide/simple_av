# Whether the data is from RSU (true) or vehicle-mounted sensors (false)
bool is_from_rsu

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

# Direction of the object (above, behind, left, right)
std_msgs/String relative_direction

# x,y positions of 4 side of the vehicle
geometry_msgs/Point[4] bounding_box