import sys
sys.path.insert(0, '../')
import RoombaCI_lib

Roomba = RoombaCI_lib.Create_2("/dev/ttyS0", 115200)

imu = RoombaCI_lib.LSM9DS1_IMU # Initialize IMU

LENGTH = 500

# readingX = [0 for i in range(LENGTH)]
# readingY = [0 for i in range(LENGTH)]
# readingZ = [0 for i in range(LENGTH)]

dictionary = {
    "readingX" : [],
    "readingY" : [],
    "readingZ" : []
}

def addValue(self, key, value):
    dictionary[key].append(value)

def writeToFile(self):
    with open('results.json','w') as fp:
        json.dum(self.dictionary,fp)


for ii in range(LENGTH):
    [a, b, c] = imu.ReadMagRaw()
    a.addValue("readingX")
    b.addValue("readingY")
    c.addValue("readingZ")

for ii in range(LENGTH):
    print(reading[ii])
