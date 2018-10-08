import sys, json
sys.path.insert(0, '../')
import RoombaCI_lib
import RPi.GPIO as GPIO
import serial

GPIO.setmode(GPIO.BCM) # Use BCM pin numbering for GPIO
Roomba = RoombaCI_lib.Create_2("/dev/ttyS0", 115200)

Roomba.WakeUp(131)
Roomba.BlinkCleanLight()

if Roomba.Available() > 0:
	x = Roomba.DirectRead(Roomba.Available())

imu = RoombaCI_lib.LSM9DS1_IMU() # Initialize IMU

Roomba.Move(0, 75)
LENGTH = 500

magX = [0 for i in range(LENGTH)]
magY = [0 for i in range(LENGTH)]
magZ = [0 for i in range(LENGTH)]

accelX = [0 for i in range(LENGTH)]
accelY = [0 for i in range(LENGTH)]
accelZ = [0 for i in range(LENGTH)]

gyroX = [0 for i in range(LENGTH)]
gyroY = [0 for i in range(LENGTH)]
gyroZ = [0 for i in range(LENGTH)]


for ii in range(LENGTH):
	[a, b, c] = imu.ReadMagRaw()
	magX[ii] = a
	magY[ii] = b
	magZ[ii] = c

	[a, b, c] = imu.ReadAccelRaw()
	accelX[ii] = a
	accelY[ii] = b
	accelZ[ii] = c

	[a, b, c] = imu.ReadGyroRaw()
	gyroX[ii] = a
	gyroY[ii] = b
	gyroZ[ii] = c


print("IMU TESTING", file=open("output.txt","a"))

print("magX", file=open("output.txt","a"))
for ii in range(LENGTH):
	print("{:.3f}".format(magX[ii]), file=open("output.txt","a"), end="")
	print(", ", file=open("output.txt","a"), end="")

print("\nmagY", file=open("output.txt","a"))
for ii in range(LENGTH):
	print("{:.3f}".format(magY[ii]), file=open("output.txt","a"), end="")
	print(", ", file=open("output.txt","a"), end="")

print("\nmagZ", file=open("output.txt","a"))
for ii in range(LENGTH):
	print("{:.3f}".format(magZ[ii]), file=open("output.txt","a"), end="")
	print(", ", file=open("output.txt","a"), end="")

print("\naccelX", file=open("output.txt","a"))
for ii in range(LENGTH):
	print("{:.3f}".format(accelX[ii]), file=open("output.txt","a"), end="")
	print(", ", file=open("output.txt","a"), end="")

print("\naccelY", file=open("output.txt","a"))
for ii in range(LENGTH):
	print("{:.3f}".format(accelY[ii]), file=open("output.txt","a"), end="")
	print(", ", file=open("output.txt","a"), end="")

print("\naccelZ", file=open("output.txt","a"))
for ii in range(LENGTH):
	print("{:.3f}".format(accelZ[ii]), file=open("output.txt","a"), end="")
	print(", ", file=open("output.txt","a"), end="")

print("\ngyroX", file=open("output.txt","a"))
for ii in range(LENGTH):
	print("{:.3f}".format(gyroX[ii]), file=open("output.txt","a"), end="")
	print(", ", file=open("output.txt","a"), end="")

print("\ngyroY", file=open("output.txt","a"))
for ii in range(LENGTH):
	print("{:.3f}".format(gyroY[ii]), file=open("output.txt","a"), end="")
	print(", ", file=open("output.txt","a"), end="")

print("\ngyroZ", file=open("output.txt","a"))
for ii in range(LENGTH):
	print("{:.3f}".format(gyroZ[ii]), file=open("output.txt","a"), end="")
	print(", ", file=open("output.txt","a"), end="")

Roomba.Move(0,0)
Roomba.ShutDown()
GPIO.cleanup()
