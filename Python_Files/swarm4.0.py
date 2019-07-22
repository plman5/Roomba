import multiprocessing
import numpy as np
from multiprocessing import Queue

''' script.py
Purpose: Code to test our roomba program;
IMPORTANT: Must be run using Python 3 (python3)
Last Modified: 7/3/2019
'''
## Import libraries ##
import serial
import math
import time
import RPi.GPIO as GPIO
import RoombaCI_lib

## Variables and Constants ##
# LED pin numbers
yled = 5
rled = 6
gled = 13
micOne=17
micTwo=22
micThree=27
reset=24
#notHeard=0.01
#oneNotHeard=True
#twoNotHeard=True
#threeNotHeard=True
#notHeards=[True,True,True]
#lastHeard=-1
statusOne=0
statusTwo=0
statusThree=0
times=[0,0,0]
first=[0,0]
second=[0,0]
third=[0,0]
cSound=343
x1=75
x2=75
x3=-150
y1=-129.9038
y2=129.9038
y3=0

## Functions and Definitions ##
''' Displays current date and time to the screen
    '''
def DisplayDateTime():
    # Month day, Year, Hour:Minute:Seconds
    date_time = time.strftime("%B %d, %Y, %H:%M:%S", time.gmtime())
    print("Program run: ", date_time)

def timedReset():
    GPIO.output(reset,GPIO.LOW)
    time.sleep(1)
    GPIO.output(reset,GPIO.HIGH)
    
def matrixMethod(t12, t23, t13, c):
    x1=75
    x2=75
    x3=-150
    y1=-129.9038
    y2=129.9038
    y3=0
    #m1=np.matrix0 y2-y1; x3-x1 y3-y1')
    m1=np.array([[0,y2-y1],[x3-x1, y3-y1]])
    minv=np.linalg.inv(m1)
    #m2=np.matrix('c*t12; c*t13')
    m2=np.array([[c*t12],[c*t13]])
    #m3=m2*minv
    m3=np.matmul(m2,minv)
    #slope=list(m3).index(0)/list(m3).index(1)
    slope=m3[0][0]/m3[1][0]
    ang=math.atan2(m3[0][0], m3[1][0])
    return(ang,slope)
    
    
    
def triangulate(t12,t23,t13,c):#1-2=12
    
    x1=75
    x2=75
    x3=-150
    y1=-129.9038
    y2=129.9038
    y3=0
    
    a12=0.5*343*t12
    b12=math.sqrt(c**2-a12**2)
    
    
    a23=0.5*343*t23
    b23=math.sqrt(c**2-a23**2)
     
    a13=0.5*343*t13
    b13=math.sqrt(c**2-a13**2)
    
    if t12>=0:
        if t13<=0:
            quad=1
            quad2=3.5
            quad3=2
        elif t23>=0:
            quad=2
            quad2=1
            quad3=1.5
        else: 
            quad=1.5
            quad2=4
            quad3=3
    elif t23<=0:
        quad=4
        quad2=3
        quad3=1.5
    elif t13>=0:
        quad=3
        quad2=1.5
        quad3=4
    else:
        quad=3.5
        quad2=2
        quad3=1
    asyAngle=0
    if quad==1:
        asyAngle=math.atan(a12/b12)
    elif quad==2:
        asyAngle=math.atan(-a12/b12)+math.pi
    elif quad==3:
        asyAngle=math.atan(a12/b12)+math.pi
    elif quad==4:
        asyAngle=math.atan(-a12/b12)
    asyAngle2=0
    if quad2==1:
        asyAngle2=math.atan(a23/b23)+(2*math.pi/3)
    elif quad2==2:
        asyAngle2=math.atan(-a23/b23)+(5*math.p1/3)
    elif:
        asyAngle2=math.atan(a23/a23)+(5*math.pi/3)
    elif:
        asyAngle=math.atan(-a23/b23)+(2*math.pi/3)
    asyAngle3=0
    if quad3==1:
        asyAngle3=math.atan(a13/b13)+(4*math.pi/3)
    elif quad3==2:
        asyAngle3=math.atan(-a13/b13)+(math.p1/3)
    elif quad3==3:
        asyAngle3=math.atan(a13/a13)+(math.pi/3)
    elif quad3==4:
        asyAngle3=math.atan(-a13/b13)+(4*math.pi/3)
    
    if asyAngle==0:
        #matrixMath(ang1, ang2,x1,x2,x3,y1,y2,y3)
        cos1=math.cos(ang2)
        cos2=math.cos(ang3)
        sin1=math.sin(ang2)
        sin2=math.sin(ang3)
        m1=np.array([[cos1,-cos2],[sin1,-sin2]])
        minv=np.linalg.inv(m1)
        m2=np.array([[(x1+x3)/2-(x2+x3)/2],[(y1+y3)/2-(y2+y3)/2]])
        m3=np.matmual(m2,minv)
        w1=m3[0][0]
        #w2=m3[1][0]
        m4=np.matrix([[w1*cos1],[w1*sin1]])
        m5=np.matrix([(x2+x3)/2],[(y2+y3)/2]])
        final=np.matrix.sum(m4, m5)
        x=final[0][0]
        y=final[1][0]
        ansAngle=atan2(y,x)#angle to target
    elif asyAngle2==0:
        #matrixMath(ang1, ang2,x1,x2,x3,y1,y2,y3)
        cos1=math.cos(ang3)
        cos2=math.cos(ang1)
        sin1=math.sin(ang3)
        sin2=math.sin(ang1)
        m1=np.array([[cos1,-cos2],[sin1,-sin2]])
        minv=np.linalg.inv(m1)
        m2=np.array([[(x1+x2)/2-(x1+x3)/2],[(y1+y2)/2-(y1+y3)/2]])
        m3=np.matmual(m2,minv)
        w1=m3[0][0]
        #w2=m3[1][0]
        m4=np.matrix([[w1*cos1],[w1*sin1]])
        m5=np.matrix([(x1+x3)/2],[(y1+y3)/2]])
        final=np.matrix.sum(m4, m5)
        x=final[0][0]
        y=final[1][0]
        ansAngle=atan2(y,x)#angle to target
    elif asyAngle3==0:
        #matrixMath(ang1, ang2,x1,x2,x3,y1,y2,y3)
        cos1=math.cos(ang1)
        cos2=math.cos(ang2)
        sin1=math.sin(ang1)
        sin2=math.sin(ang2)
        m1=np.array([[cos1,-cos2],[sin1,-sin2]])
        minv=np.linalg.inv(m1)
        m2=np.array([[(x2+x3)/2-(x1+x2)/2],[(y2+y3)/2-(y1+y2)/2]])
        m3=np.matmual(m2,minv)
        w1=m3[0][0]
        #w2=m3[1][0]
        m4=np.matrix([[w1*cos1],[w1*sin1]])
        m5=np.matrix([(x1+x2)/2],[(y1+y2)/2]])
        final=np.matrix.sum(m4, m5)
        x=final[0][0]
        y=final[1][0]
        ansAngle=atan2(y,x)#angle to target
        
    
def matrixMath(ang1, ang2,x1,x2,x3,y1,y2,y3)    
    cos1=math.cos(ang1)
    cos2=math.cos(ang2)
    sin1=math.sin(ang1)
    sin2=math.sin(ang2)
    m1=np.array([[cos1,-cos2],[sin1,-sin2]])
    minv=np.linalg.inv(m1)
    m2=np.array([[(x2+x3)/2-(x1+x2)/2],[(y2+y3)/2-(y1+y2)/2]])
    m3=np.matmual(m2,minv)
    w1=m3[0][0]
    #w2=m3[1][0]
    m4=np.matrix([[w1*cos1],[w1*sin1]])
    m5=np.matrix([(x1+x2)/2],[(y1+y2)/2]])
    final=np.matrix.sum(m4, m5)
    x=final[0][0]
    y=final[1][0]
    ansAngle=atan2(y,x)#angle to target
    return ansAngle
def checkMic(cue,pin, mic, times):
    status=0
    while status==0:
        status=GPIO.input(pin)
        #print(time.time()-startloop)
    cue.put([mic-1, time.time()])

## -- Code Starts Here -- ##
# Setup Code #
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering for GPIO
DisplayDateTime() # Display current date and time

# LED Pin setup
GPIO.setup(yled, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(rled, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(gled, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(micOne, GPIO.IN, pull_up_down= GPIO.PUD_UP)##Check for initial later
GPIO.setup(micTwo, GPIO.IN,  pull_up_down= GPIO.PUD_UP)
GPIO.setup(micThree, GPIO.IN, pull_up_down= GPIO.PUD_UP)
GPIO.setup(reset, GPIO.OUT, initial=GPIO.LOW)
#statusOneTwo=0
#statusTwoTwo=0
#statusThreeTwo=0
#stuck=False
startloop=0

#with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
#        executor.map(thread_function, range(3))

GPIO.output(reset,GPIO.LOW)
startTime=time.time()
timeBase=time.time()
GPIO.output(reset, GPIO.HIGH)
# one=threading.Thread(target=checkMic, args=(micOne, 1,times), daemon=False)
# two=threading.Thread(target=checkMic, args=(micTwo, 2,times), daemon=False)
# three=threading.Thread(target=checkMic, args=(micThree, 3,times), daemon=False)
# threads=[]
# threads.append(one)
# threads.append(two)
# threads.append(three)
q=Queue()
one=multiprocessing.Process(target=checkMic, args=(q,micOne,1,times,))
two=multiprocessing.Process(target=checkMic, args=(q,micTwo,2,times,))
three=multiprocessing.Process(target=checkMic, args=(q,micThree,3,times,))
mps=[]
mps.append(one)
mps.append(two)
mps.append(three)
while True:
    try:
        startloop=time.time()
        for p in mps:
            p.start()
            print("started")
        # for t in threads:
            # t.join()
        start=time.time()
        lights=False
        while q.qsize() <3:
            GPIO.output(gled,GPIO.HIGH)
            GPIO.output(yled,GPIO.HIGH)
            GPIO.output(rled,GPIO.HIGH)
            # start=time.time()
            # while time.time()-1<start:
            if (time.time()-start)>4.0:
                start=start+4
            if lights:
                GPIO.output(gled,GPIO.LOW)
                GPIO.output(yled,GPIO.LOW)
                GPIO.output(rled,GPIO.LOW)
            else:
                GPIO.output(gled,GPIO.HIGH)
                GPIO.output(yled,GPIO.HIGH)
                GPIO.output(rled,GPIO.HIGH)
        GPIO.output(gled,GPIO.LOW)
        GPIO.output(yled,GPIO.LOW)
        GPIO.output(rled,GPIO.LOW)
        first=q.get()
        second=q.get()
        third=q.get()
    #if not first[0] ==-1:
        times[first[0]]=first[1]
    #if not second[0] ==-1:
        times[second[0]]=second[1]
    #if not third[0] ==-1:
        times[third[0]]=third[1]
        if max(times)-min(times)>0.002:
            print("Nah fam")
            times=[0,0,0]
        else:
            print("T1-T2: {0:.7f}".format(1000*(times[0]-times[1])))
            print("T2-T3: {0:.7f}".format(1000*(times[1]-times[2])))
            print("T1-T3: {0:.7f}".format(1000*(times[0]-times[2])))
            if times[0]<times[1] and times[0]<times[2]:
                if times[1]<times[2]:
                    print("123")
                else:
                    print("132")
            elif times[1]<times[0] and times[1]<times[2]:
                if times[0]<times[2]:
                    print("213")
                else:
                    print("231")
            elif times[2]<times[1] and times[2]<times[0]:
                if times[1]<times[0]:
                    print("321")
                else:
                    print("312")
            #time.sleep(0.5)
            #calculations go here
        #q=Queue()
            slope,angle=matrixMethod(times[0]-times[1],times[1]-times[2],times[0]-times[2],cSound)
            print("slope matrix:",slope)
            print("angle matrix:",angle)
            angle= triangulate(times[0]-times[1],times[1]-times[2],times[0]-times[2],cSound))
            print("angle hyperbola",angle)
        one=multiprocessing.Process(target=checkMic, args=(q,micOne,1,times,))
        two=multiprocessing.Process(target=checkMic, args=(q,micTwo,2,times,))
        three=multiprocessing.Process(target=checkMic, args=(q,micThree,3,times,))
        mps=[]
        mps.append(one)
        mps.append(two)
        mps.append(three)
        times=[0,0,0]
        first=[0,0]
        second=[0,0]
        third=[0,0]
        timedReset()
            #stuck=False 
        #    print("Mic One: {0}".format(statusOne))
        #    print("Mic Two: {0}".format(statusTwo))
        #    print("Mic Three: {0}".format(statusThree))
        #time.sleep(0.1)  
        # if time.time()-timeBase>1.0:
            # print(time.time()-startloop)
            # timeBase=timeBase+1
            #   time.sleep(1)
    except KeyboardInterrupt:
        break
GPIO.output(reset,GPIO.LOW)

'''
# Wake Up Roomba Sequence
GPIO.output(gled, GPIO.HIGH) # Turn on green LED to say we are alive
print(" Starting ROOMBA... ")
Roomba = RoombaCI_lib.Create_2("/dev/ttyS0", 115200)
Roomba.ddPin = 23 # Set Roomba dd pin number
GPIO.setup(Roomba.ddPin, GPIO.OUT, initial=GPIO.LOW)
Roomba.WakeUp(131) # Start up Roomba in Safe Mode
# 131 = Safe Mode; 132 = Full Mode (Be ready to catch it!)
Roomba.BlinkCleanLight() # Blink the Clean light on Roomba

if Roomba.Available() > 0: # If anything is in the Roomba receive buffer
	x = Roomba.DirectRead(Roomba.Available()) # Clear out Roomba boot-up info
	#print(x) # Include for debugging

print(" ROOMBA Setup Complete")
GPIO.output(yled, GPIO.HIGH) # Indicate within setup sequence
# Initialize IMU
print(" Starting IMU...")
imu = RoombaCI_lib.LSM9DS1_I2C() # Initialize IMU
time.sleep(0.1)
# Clear out first reading from all sensors
x = imu.magnetic
x = imu.acceleration
x = imu.gyro
# Calibrate IMU
print(" Calibrating IMU...")
Roomba.Move(0,75) # Start Roomba spinning
imu.CalibrateMag() # Calculate magnetometer offset values
Roomba.Move[0,0] # Stop Roomba spinning
time.sleep(0.5)
imu.CalibrateGyro() # Calculate gyroscope offset values
# Display offset values
print("mx_offset = {:f}; my_offset = {:f}; mz_offset = {:f}"\
	.format(imu.m_offset[0], imu.m_offset[1], imu.m_offset[2]))
print("gx_offset = {:f}; gy_offset = {:f}; gz_offset = {:f}"\
	.format(imu.g_offset[0], imu.g_offset[1], imu.g_offset[2]))
print(" IMU Setup Complete")
time.sleep(3) # Gives time to read offset values before continuing
GPIO.output(yled, GPIO.LOW) # Indicate setup sequence is complete

if Xbee.inWaiting() > 0: # If anything is in the Xbee receive buffer
    x = Xbee.read(Xbee.inWaiting()).decode() # Clear out Xbee input buffer
    #print(x) # Include for debugging

# Main Code #


## -- Ending Code Starts Here -- ##
# Make sure this code runs to end the program cleanly

Roomba.ShutDown() # Shutdown Roomba serial connection
Xbee.close()
'''
GPIO.cleanup() # Reset GPIO pins for next program