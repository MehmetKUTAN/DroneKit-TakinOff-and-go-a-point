# DroneKit-TakinOff-and-go-a-point


This code explains how to air your Copter.
The code below shows the function of arming, taking off and flying a Helicopter to a certain altitude

These checks are encapsulated by the attribute, which is true when the vehicle has booted, EKF is ready, and the vehicle has GPS lock.

Once the vehicle is ready we set the mode to GUIDED and arm it.
 
The takeoff command is asynchronous and may be interrupted if another command arrives before the target altitude is reached and to correct these problems, wait until the vehicle reaches a certain height before the function returns.

