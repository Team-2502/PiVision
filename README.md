# PiVision

## What is it?

This is code written for the 2017 FRC challenge FIRST Steamworks. This code figures out how off-center the vision target is from the camera. 
This data is sent to the robot via NetworkTables (a library specific to FRC). 

## How do I use it?

You will need

1. A Raspberry Pi with OpenCV and Python 3
2. A microUSB to USB A cable
3. An ethernet cable
4. An FRC robot. 

To use it

1. Put this code on the Raspberry Pi, and add a cron job to run Vision.py every minute or so

2. Attach the Pi to the robot with some velcro

3. Plug one end of the ethernet cable into the Pi, and the other into the 2nd port on the router. This way, it can connect to the RoboRIO.

4. Plug the microUSB end of the cable into the Pi, and the other end into the RoboRIO. Alternatively, snip off the USB A end, strip + crimp the power wires, and plug them into the 5V/2A slot on the VRM.

5. Use the info on Network Tables in your robot code. [Example from 2017](https://github.com/Team-2502/UpdatedRobotCode2017/blob/d33ca36bb2aa7d9b5ec2c0353cd1bb7cbfa21d8e/src/com/team2502/robot2017/subsystem/VisionSubsystem.java)
