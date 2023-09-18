# mediapipe_door_opener
![This is an example of the mediapipe hand detection window][

## Overview
I utilized the Mediapipe library to discern whether a hand was open or clenched. Subsequently, this data was transmitted via a socket to another program running on a Raspberry Pi 4. This secondary program then operated the door, opening it when the hand was open and closing it when clenched. The main program is titled 'Hand_Pose_Detection.py' which collects, analyzes, and sends data via socket to the second program titled 'Door_Open_close.py'. This program then uses the data to determine if the door should be opened, closed or left still. 

A few things to note:
- 'Hand_Pose_Detection.py' processes a frame every 0.3 seconds. This is to ensure that there isn't a growing delay between the door opener trying to keep up, and the computer constantly sending data to it.
- The code uses a value of 3 for determining if the hand is closed or opened, depending on your hand size that value will need to change (line 51). An easy way to see what this indicator should be for your hand size is to put in the line before 51: ```print(value)``` Then when you open and close your hand you will be able to see the data. For example if when you closed your hand it said 2.765... and when your hand was closed it was 1.546... then you could use 2 as the benchmark value.

## Intergrating the code 

## Application

