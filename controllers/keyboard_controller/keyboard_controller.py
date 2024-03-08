from controller import Robot, Motor, Lidar, Keyboard, LidarPoint, Camera
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle

# Constants
MAX_SPEED = 6.67

# Initialize Webots robot
robot = Robot()
plt.ion()
# Setup devices (assuming device names and Webots setup)
timestep = int(robot.getBasicTimeStep())
camera = robot.getDevice('camera')
camera.enable(timestep)
camera.recognitionEnable(timestep)
leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)
lidar = robot.getDevice("LDS-01")
lidar.enable(timestep)
lidar.enablePointCloud()
keyboard = robot.getKeyboard()
keyboard.enable(timestep)

# Initialize plot for LIDAR data visualization
fig, ax = plt.subplots(figsize=(10, 10))
lidar_data_line, = ax.plot([], [], 'bo', markersize=1)  # Blue line for LIDAR data points
ax.set_xlim(-7, 7)  # Assuming LIDAR range is normalized [-1, 1]
ax.set_ylim(-7, 7)
ax.set_title('LIDAR Readings')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.axis('equal')
ax.axis('off')

# Add a black circle of size 5 at (0,0)
circle = Circle((0, 0), 0.1, color='black', fill=False)  # 'fill=False' if you want it unfilled
short_line = Line2D([0, 0], [0, 0.1], color='black')
ax.add_line(short_line)
ax.add_patch(circle)

# # Function to update LIDAR data in the plot
# def update_lidar_plot(color_index_dict):
#     lidar_points = lidar.getRangeImage()  # Fetch LIDAR data
#     # Assuming lidar_points are polar coordinates, convert to Cartesian
#     angles = np.linspace(-np.pi, np.pi, len(lidar_points)) + np.pi / 2
#     x = lidar_points * np.cos(angles) * -1
#     y = lidar_points * np.sin(angles)
#     #lidar_data_line.set_data(x, y)
#     # Plot each point
#     for i in range(len(x)):
#         # Determine the color for the current point
#         point_color = 'gray'
#         for color, indices in color_index_dict.items():
#             if i in indices:
#                 point_color = color
#                 break

#         ax.plot(x[i], y[i], 'o', markersize=1, color=point_color)
#     plt.draw()
#     plt.pause(0.001)  # Pause briefly to update the plot


# Function to update LIDAR data in the plot
def update_lidar_plot():
    lidar_points = lidar.getRangeImage()  # Fetch LIDAR data
    # Assuming lidar_points are polar coordinates, convert to Cartesian
    angles = np.linspace(-np.pi, np.pi, len(lidar_points)) + np.pi / 2
    x = lidar_points * np.cos(angles) * -1
    y = lidar_points * np.sin(angles)
    lidar_data_line.set_data(x, y)
    plt.draw()
    plt.pause(0.001)  # Pause briefly to update the plot



# Main control loop
while robot.step(timestep) != -1:
    # Robot control code here (handling keyboard input, motor speed adjustments, etc.)
    key = keyboard.getKey()
    while keyboard.getKey() != -1: pass

    if key == Keyboard.UP:
        # Move forward
        leftMotor.setVelocity(MAX_SPEED)
        rightMotor.setVelocity(MAX_SPEED)
    elif key == Keyboard.DOWN:
        # Move backward
        leftMotor.setVelocity(-MAX_SPEED)
        rightMotor.setVelocity(-MAX_SPEED)
    elif key == Keyboard.LEFT:
        # Turn left
        leftMotor.setVelocity(-MAX_SPEED / 2)
        rightMotor.setVelocity(MAX_SPEED / 2)
    elif key == Keyboard.RIGHT:
        # Turn right
        leftMotor.setVelocity(MAX_SPEED / 2)
        rightMotor.setVelocity(-MAX_SPEED / 2)
    else:
        # Stop
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)


    # Update LIDAR visualization
    update_lidar_plot()

    # Get current number of object recognized
    number_of_objects = camera.getRecognitionNumberOfObjects()
    print("\nRecognized {} objects.\n".format(number_of_objects))

    # Get and display all the objects information
    objects = camera.getRecognitionObjects()
    for i, obj in enumerate(objects):
        print("Model of object {}: {}".format(i, obj.getModel()))
        print("Id of object {}: {}".format(i, obj.getId()))
        print("Relative position of object {}: {} {} {}".format(i, *obj.getPosition()))
        print("Relative orientation of object {}: {} {} {} {}".format(i, *obj.getOrientation()))
        print("Size of object {}: {} {}".format(i, *obj.getSize()))
        print("Position of the object {} on the camera image: {} {}".format(i, *obj.getPositionOnImage()))
        print("Size of the object {} on the camera image: {} {}".format(i, *obj.getSizeOnImage()))
        for j in range(obj.getNumberOfColors()):
            colors = obj.getColors()
            print("- Color {}/{}: {} {} {}".format(j + 1, obj.getNumberOfColors(), 
                                                    colors[3 * j], colors[3 * j + 1], colors[3 * j + 2]))

    

