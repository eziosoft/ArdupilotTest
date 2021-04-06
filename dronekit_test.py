from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative, mavutil

# Connect to the Vehicle (in this case a TCP endpoint) - w realu bedzie to polaczenie przez UART
vehicle = connect('tcp:192.168.138.131:5763', wait_ready=True)

def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Home Location:", vehicle.home_location)
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

#ustawia heading         
def condition_yaw(heading, relative=False):
    if relative:
        is_relative=1 #yaw relative to direction of travel
    else:
        is_relative=0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0, #confirmation
        heading,    # param 1, yaw in degrees
        0,          # param 2, yaw speed deg/s
        1,          # param 3, direction -1 ccw, 1 cw
        is_relative, # param 4, relative offset 1, absolute angle 0
        0, 0, 0)    # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)

#Lec na pozycje i czekaj az zostanie osiagnieta - jak na razie nie znalazlem lepszego rozwiazania
def goto_location(waypoint):
    vehicle.simple_goto(waypoint)
    time.sleep(2)
    reached = 0
    while(not reached):
        time.sleep(1)
        a = vehicle.velocity
        if (abs(a[1])< 0.2 and abs(a[2])< 0.2 and abs(a[0])< 0.2):
            reached = 1
    print ("Waypoint reached!")





#Start
arm_and_takeoff(2)

print("Set default/target airspeed to 3")
vehicle.airspeed = 3

print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(-35.3632928,149.1652374, 100)
goto_location(point1)


# default home position LocationGlobal:lat=-35.3632621,lon=149.1652374,alt=583.99
print("Going towards second point")
home = LocationGlobalRelative(-35.3632621, 149.1652374, 5)
goto_location(home)

#set yaw to known value - aby ladowac ciagle w tej samej pozycji
condition_yaw(45)

time.sleep(3000)

#Land
vehicle.mode = VehicleMode("LAND")

# Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()


# print("Returning to Launch")
# vehicle.mode = VehicleMode("RTL")