from controller import Robot, Keyboard, Motor

# Constants
MAX_SPEED = 6.28

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
lidar = robot.getLidar("LDS-01")
lidar.enable(timestep)
lidar.enablePointCloud()

# Enable keyboard
keyboard = robot.getKeyboard()
keyboard.enable(timestep)

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
    lidarData = lidar.getRangeImage()
    print("LIDAR readings:", lidarData)

# Enter here exit cleanup code
