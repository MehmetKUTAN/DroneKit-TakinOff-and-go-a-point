from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative, Command
from pymavlink import mavutil
import time
import math
import dronekit_sitl
import argparse
parser = argparse.ArgumentParser(description='Control Copter and send commands in GUIDED mode ')
parser.add_argument('--connect',bound=1156000)  #your bound number
args = parser.parse_args()
connection_string = args.connect
sitl = None

# Start SITL if no connection string specified
if not connection_string:
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()

# Connect to the Vehicle
print ('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True,baud=57600)


#***************************************************************************
def battery_check():
    print ("Battery: %s" % vehicle.battery.voltage)
    if(vehicle.battery.voltage < 12):
        print ("Battery Low. Landing")
    land()

def land():
    print("Vehicle in LAND mode")
    vehicle.mode = VehicleMode("LAND")
    while not vehicle.location.global_relative_frame.alt==0:
        if vehicle.location.global_relative_frame.alt < 2:
            set_velocity_body(vehicle,0,0,0.1)
    vehicle.armed = False
    vehicle.close()

def temp_land():
    print("Vehicle in LAND mode")
    vehicle.mode = VehicleMode("LAND")
    while not vehicle.location.global_relative_frame.alt==0:
        if vehicle.location.global_relative_frame.alt < 2:
            set_velocity_body(vehicle,0,0,0.1)
        print ("Vehicle in AUTO mode")
    vehicle.mode = VehicleMode("AUTO")

#***************************************************************************

def set_velocity_body(vehicle, vx, vy, vz):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
    0,
    0, 0,
    mavutil.mavlink.MAV_FRAME_BODY_NED,
    0b0000111111000111,  # -- BITMASK -> Consider only the velocities
    0, 0, 0,  # -- POSITION
    vx, vy, vz,  # -- VELOCITY
    0, 0, 0,  # -- ACCELERATIONS
    0, 0)
    vehicle.send_mavlink(msg)
    vehicle.flush()
#***************************************************************************

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

#***************************************************************************
def goto_location_target(waypoint):
    vehicle.simple_goto(waypoint)
    time.sleep(2)
    reached = 0
    while(not reached):
        time.sleep(1)
        a = vehicle.velocity
        if (abs(a[1])< 0.2 and abs(a[2])< 0.2 and abs(a[0])< 0.2):
            reached = 1
    print ("Waypoint reached!")


############# RETURN TO HOME LAND MODE ##########
def rtl_mode():
    print("Vehicle Returning to LAND mode")
    vehicle.mode = VehicleMode("RTL")


###################################################################################
################################ START CODE #######################################
###################################################################################

############# POINTS ###############
location_target = LocationGlobalRelative(24.830125, 67.097387, 15)
############# ARM AND TAKE OFF #############
arm_and_takeoff(15)                                                                                                 # Vehicle takeoff
location_home = vehicle.location.global_frame                                                                                #HOME
print ("Reached Target Altitude")
print ("Altitude: ", vehicle.location.global_relative_frame.alt)
print ("Home Location: %s" % location_home)

############# POINT 1 ###9###########
print ("Going to location_target")
goto_location_target(location_target)
print ("Reached location_target")
print ("Location: %s" % vehicle.location.global_frame)

battery_check()

############### LAND ################
temp_land()

############ RETURN TO HOME ##########
print ("Going to Home")
goto_location_target(location_home)
print ("Reached Home")
print ("Location: %s" % vehicle.location.global_frame)
battery_check()


############# LAND #################    
rtl_mode()                                                                                                               # Land vehicle once mission is over
vehicle.flush()
vehicle.close()
print ("Exiting Script")


###################################################################################
################################# END CODE ########################################
###################################################################################