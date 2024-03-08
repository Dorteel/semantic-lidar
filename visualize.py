from controller import Robot, Motor, Lidar, Keyboard, LidarPoint
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Constants
MAX_SPEED = 6.67

# Initialize Webots robot
robot = Robot()

# Setup devices (assuming device names and Webots setup)
timestep = int(robot.getBasicTimeStep())
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
fig, ax = plt.subplots(figsize=(8, 8))
lidar_data_line, = ax.plot([], [], 'r-')  # Red line for LIDAR data points
ax.set_xlim(-1, 1)  # Assuming LIDAR range is normalized [-1, 1]
ax.set_ylim(-1, 1)
ax.set_title('LIDAR Readings')
ax.set_xlabel('X Coordinate')
ax.set_ylabel('Y Coordinate')
ax.axis('equal')

# Function to update LIDAR data in the plot
def update_lidar_plot():
    lidar_points = lidar.getRangeImage()  # Fetch LIDAR data
    # Assuming lidar_points are polar coordinates, convert to Cartesian
    angles = np.linspace(-np.pi, np.pi, len(lidar_points))
    x = lidar_points * np.cos(angles)
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
        leftMotor.setVelocity(-MAX_SPEED)
        rightMotor.setVelocity(MAX_SPEED)
    elif key == Keyboard.RIGHT:
        # Turn right
        leftMotor.setVelocity(MAX_SPEED)
        rightMotor.setVelocity(-MAX_SPEED)
    else:
        # Stop
        leftMotor.setVelocity(0)
        rightMotor.setVelocity(0)
    # Update LIDAR visualization
    update_lidar_plot()
