import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib

GpioPins = [18, 23, 24, 25]

# Declare a named instance of class pass a name and motor type
mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")


# call the function pass the parameters

#send 5 step signals 50 times in each direction.
for i in range(50):
    mymotortest.motor_run(GpioPins , 0.002, 10, False, False, "half", .05)
for i in range(50):
    mymotortest.motor_run(GpioPins , 0.002, 10, True, False, "half", .05)

# good practise to cleanup GPIO at some point before exit
GPIO.cleanup()