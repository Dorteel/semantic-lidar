# Copyright 1996-2023 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from controller import Robot, Camera, Motor

SPEED = 1.5
TIME_STEP = 64

def run_robot(robot):
    # Get the camera device, enable it and the recognition
    camera = robot.getDevice('camera')
    camera.enable(TIME_STEP)
    camera.recognitionEnable(TIME_STEP)

    # get a handler to the motors and set target position to infinity (speed control)
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))

    # Set the motors speed
    left_motor.setVelocity(-SPEED)
    right_motor.setVelocity(SPEED)

    # Main loop
    while robot.step(TIME_STEP) != -1:
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

if __name__ == "__main__":
    robot = Robot()
    run_robot(robot)
