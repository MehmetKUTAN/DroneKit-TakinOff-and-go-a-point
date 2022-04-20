# DroneKit-TakinOff-and-go-a-point
MehmetKUTAN/DroneKit-TakinOff-and-go-a-point

This code explains how to air your Copter.
The code below shows the function of arming, taking off and flying a Helicopter to a certain altitude
""""""
def arm_and_takeoff(aTargetAltitude):
    print ("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print (" Waiting for vehicle to initialise...")
        vehicle.arm()
        time.sleep(1)
    print ("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        print (" Waiting for arming...")
        time.sleep(1)
    print ("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude
    while True:
        print (" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:  # Trigger just below target alt.
            print ("Reached target altitude")
            break
        time.sleep(1)
""""

These checks are encapsulated by the attribute, which is true when the vehicle has booted, EKF is ready, and the vehicle has GPS lock.
 print ("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print (" Waiting for vehicle to initialise...")
        vehicle.arm()
        time.sleep(1)

Once the vehicle is ready we set the mode to GUIDED and arm it.
 print ("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        print (" Waiting for arming...")
        time.sleep(1)
    print ("Taking off!")
vehicle.simple_takeoff(aTargetAltitude)

The takeoff command is asynchronous and may be interrupted if another command arrives before the target altitude is reached and to correct these problems, wait until the vehicle reaches a certain height before the function returns.
vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude
    while True:
        print (" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:  # Trigger just below target alt.
            print ("Reached target altitude")
            break
        time.sleep(1)
