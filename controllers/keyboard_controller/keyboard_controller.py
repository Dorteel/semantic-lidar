from controller import Robot, Keyboard, Motor, LidarPoint, ContactPoint, Camera
import matplotlib.pyplot as plt
import numpy as np

# Constants
MAX_SPEED = 6.67

# Create robot instance
robot = Robot()

# Get timestep
timestep = int(robot.getBasicTimeStep())

# Initialize motors
leftMotor = robot.getDevice("left wheel motor")
rightMotor = robot.getDevice("right wheel motor")
leftMotor.setPosition(float('inf'))  # Set to infinity for velocity control
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

# Initialize LIDAR
lidar = robot.getDevice("LDS-01")
camera = robot.getDevice("camera")
lidar.enable(timestep)
lidar.enablePointCloud()
camera.enable(timestep)
camera.recognitionEnable(timestep)
# Enable keyboard
keyboard = robot.getKeyboard()
keyboard.enable(timestep)


def polar_to_cartesian(r, theta):
    """Convert polar coordinates to Cartesian coordinates."""
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def plot_lidar_readings(ranges, angles):
    """Plot LIDAR readings."""
    x_coords, y_coords =  list(zip(*ranges))#polar_to_cartesian(ranges, angles)
    #x_coords, y_coords = polar_to_cartesian(ranges, angles)

    plt.figure(figsize=(8, 8))
    plt.plot(x_coords, y_coords, 'o', markersize=2)
    plt.title('LIDAR Readings')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.axis('equal')
    plt.show()


# Main loop
while robot.step(timestep) != -1:
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

    # LIDAR data processing
    lidarData = [[p.x, p.y] for p in lidar.getPointCloud()]
    img = camera.getImage()
    #print(len(lidarData))
    #print("LIDAR readings:", lidarData)
    print(camera.getRecognitionObjects())
    # lidar_ranges = np.random.uniform(low=0.5, high=10.0, size=360)
    lidar_angles = np.linspace(-np.pi, np.pi, 360)
    # Plot the LIDAR readings
    #plot_lidar_readings(lidarData, lidar_angles)
    
# Enter here exit cleanup code
