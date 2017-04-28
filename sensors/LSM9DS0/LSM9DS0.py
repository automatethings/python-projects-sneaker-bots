import sys
import os
import math

# needed in order to import Adafruit library a few directories back
sys.path.append(sys.path.append('/'.join(os.getcwd().split('/')[:-4])))

import Adafruit.GPIO.I2C as I2C



class LSM9DS0(object):
    # set global variables
    # The same address is used for both the magnetometer and accelerometer, but
    # each has their own variable, to avoid confusion.
    LSM9DS0_MAG_ADDRESS	    =   0x1D
    LSM9DS0_ACCEL_ADDRESS	=	0x1D
    LSM9DS0_GYRO_ADDRESS    =   0x6B

    #LSM9DS0 gyrometer registers
    LSM9DS0_WHO_AM_I_G	      =	0x0F
    LSM9DS0_CTRL_REG1_G	      =	0x20
    LSM9DS0_CTRL_REG3_G	      =	0x22
    LSM9DS0_CTRL_REG4_G	      =	0x23
    LSM9DS0_OUT_X_L_G	      =	0x28
    LSM9DS0_OUT_X_H_G	      =	0x29
    LSM9DS0_OUT_Y_L_G	      =	0x2A
    LSM9DS0_OUT_Y_H_G	      =	0x2B
    LSM9DS0_OUT_Z_L_G	      =	0x2C
    LSM9DS0_OUT_Z_H_G	      =	0x2D

    # LSM9DS0 temperature addresses
    LSM9DS0_OUT_TEMP_L_XM	  =	0x05
    LSM9DS0_OUT_TEMP_H_XM	  =	0x06

    # Magnetometer addresses
    LSM9DS0_STATUS_REG_M	  =	0x07
    LSM9DS0_OUT_X_L_M         =	0x08
    LSM9DS0_OUT_X_H_M         =	0x09
    LSM9DS0_OUT_Y_L_M         =	0x0A
    LSM9DS0_OUT_Y_H_M         =	0x0B
    LSM9DS0_OUT_Z_L_M         =	0x0C
    LSM9DS0_OUT_Z_H_M         =	0x0D

    # Shared addresses
    LSM9DS0_WHO_AM_I_XM	      =	0x0F
    LSM9DS0_INT_CTRL_REG_M    =	0x12
    LSM9DS0_INT_SRC_REG_M	  =	0x13
    LSM9DS0_CTRL_REG1_XM      =	0x20
    LSM9DS0_CTRL_REG2_XM	  =	0x21
    LSM9DS0_CTRL_REG5_XM	  =	0x24
    LSM9DS0_CTRL_REG6_XM	  =	0x25
    LSM9DS0_CTRL_REG7_XM	  =	0x26

    # Accelerometer addresses
    LSM9DS0_OUT_X_L_A	      =	0x28
    LSM9DS0_OUT_X_H_A	      =	0x29
    LSM9DS0_OUT_Y_L_A	      =	0x2A
    LSM9DS0_OUT_Y_H_A	      =	0x2B
    LSM9DS0_OUT_Z_L_A	      =	0x2C
    LSM9DS0_OUT_Z_H_A	      =	0x2D

    # Various settings included in the Arduino library. I haven't used these,
    # to keep to a default setting for simplicity, however, users can change
    # the settings easily.
    LSM9DS0_ACCELRANGE_2G                = 0b000 << 3
    LSM9DS0_ACCELRANGE_4G                = 0b001 << 3
    LSM9DS0_ACCELRANGE_6G                = 0b010 << 3
    LSM9DS0_ACCELRANGE_8G                = 0b011 << 3
    LSM9DS0_ACCELRANGE_16G               = 0b100 << 3

    LSM9DS0_ACCELDATARATE_POWERDOWN      = 0b0000 << 4
    LSM9DS0_ACCELDATARATE_3_125HZ        = 0b0001 << 4
    LSM9DS0_ACCELDATARATE_6_25HZ         = 0b0010 << 4
    LSM9DS0_ACCELDATARATE_12_5HZ         = 0b0011 << 4
    LSM9DS0_ACCELDATARATE_25HZ           = 0b0100 << 4
    LSM9DS0_ACCELDATARATE_50HZ           = 0b0101 << 4
    LSM9DS0_ACCELDATARATE_100HZ          = 0b0110 << 4
    LSM9DS0_ACCELDATARATE_200HZ          = 0b0111 << 4
    LSM9DS0_ACCELDATARATE_400HZ          = 0b1000 << 4
    LSM9DS0_ACCELDATARATE_800HZ          = 0b1001 << 4
    LSM9DS0_ACCELDATARATE_1600HZ         = 0b1010 << 4

    LSM9DS0_MAGGAIN_2GAUSS               = 0b00 << 5
    LSM9DS0_MAGGAIN_4GAUSS               = 0b01 << 5
    LSM9DS0_MAGGAIN_8GAUSS               = 0b10 << 5
    LSM9DS0_MAGGAIN_12GAUSS              = 0b11 << 5

    LSM9DS0_MAGDATARATE_3_125HZ          = 0b000 << 2
    LSM9DS0_MAGDATARATE_6_25HZ           = 0b001 << 2
    LSM9DS0_MAGDATARATE_12_5HZ           = 0b010 << 2
    LSM9DS0_MAGDATARATE_25HZ             = 0b011 << 2
    LSM9DS0_MAGDATARATE_50HZ             = 0b100 << 2
    LSM9DS0_MAGDATARATE_100HZ            = 0b101 << 2

    LSM9DS0_GYROSCALE_245DPS             = 0b00 << 4
    LSM9DS0_GYROSCALE_500DPS             = 0b01 << 4
    LSM9DS0_GYROSCALE_2000DPS            = 0b10 << 4

    DT                                  = 0.01
    RAD_TO_DEG                          = 57.29578  # 1 radian = 57.29578 degrees
    M_PI                                = 3.14159265358979323846
    GYRO_SENSITIVITY                    = 0.07
    gyroXangle		= 0
    gyroYangle		= 0
    gyroZangle 		= 0
    CFangleX 		= 0
    CFangleY 		= 0
    CFangleZ 		= 0

    def __init__(self,bus):
    	# grab addresses for each (gyroscope, accelerometer and magnetometer)

    	# initialize magnetometer
        self.mag    = I2C.get_i2c_device(self.LSM9DS0_MAG_ADDRESS, bus)
        self.mag.write8(self.LSM9DS0_CTRL_REG5_XM, 0b11110000) # Temperature sensor enabled, high res mag, 50Hz
        self.mag.write8(self.LSM9DS0_CTRL_REG6_XM, 0b01100000) # +/- 12 gauss
        self.mag.write8(self.LSM9DS0_CTRL_REG7_XM, 0b00000000) # Normal mode, continuous-conversion mode

    	# initialize accelerometer
        self.accel  = I2C.get_i2c_device(self.LSM9DS0_ACCEL_ADDRESS, bus)
        self.accel.write8(self.LSM9DS0_CTRL_REG1_XM, 0b01100111) # 100Hz, XYZ enabled
        self.accel.write8(self.LSM9DS0_CTRL_REG2_XM, 0b00100000) # +/- 16 g

    	# initialize gyroscope
        self.gyro   = I2C.get_i2c_device(self.LSM9DS0_GYRO_ADDRESS, bus)
        self.gyro.write8(self.LSM9DS0_CTRL_REG1_G, 0b00001111) # Normal power mode, XYZ enabled
        self.gyro.write8(self.LSM9DS0_CTRL_REG4_G, 0b00110000) # Continuous update, 2000 dps

        # initialize variables
        
        return

    def gyroscope(self):
    	# get raw gyroscope data
        gyroX = self.gyro.readU8(self.LSM9DS0_OUT_X_L_G) | self.gyro.readU8(self.LSM9DS0_OUT_X_H_G) << 8
        gyroY = self.gyro.readU8(self.LSM9DS0_OUT_Y_L_G) | self.gyro.readU8(self.LSM9DS0_OUT_Y_H_G) << 8
        gyroZ = self.gyro.readU8(self.LSM9DS0_OUT_Z_L_G) | self.gyro.readU8(self.LSM9DS0_OUT_Z_H_G) << 8

        gyroArr = [gyroX, gyroY, gyroZ]

        for i in range(len(gyroArr)):
            if gyroArr[i] > 32767:
                gyroArr[i] -= 65536

        return gyroArr

    def accelerometer(self):
    	# get raw accelerometer data
        accelX = self.accel.readU8(self.LSM9DS0_OUT_X_L_A) | self.accel.readU8(self.LSM9DS0_OUT_X_H_A) << 8
        accelY = self.accel.readU8(self.LSM9DS0_OUT_Y_L_A) | self.accel.readU8(self.LSM9DS0_OUT_Y_H_A) << 8
        accelZ = self.accel.readU8(self.LSM9DS0_OUT_Z_L_A) | self.accel.readU8(self.LSM9DS0_OUT_Z_H_A) << 8

        accelArr = [accelX, accelY, accelZ]

        # Values are signed and therefore must be checked
        for i in range(len(accelArr)):
            if accelArr[i] > 32767:
                accelArr[i] -= 65536

        return accelArr

    def magnetometer(self):
    	# get raw magnetometer data
        magX = self.mag.readU8(self.LSM9DS0_OUT_X_L_M) | self.mag.readU8(self.LSM9DS0_OUT_X_H_M) << 8
        magY = self.mag.readU8(self.LSM9DS0_OUT_Y_L_M) | self.mag.readU8(self.LSM9DS0_OUT_Y_H_M) << 8
        magZ = self.mag.readU8(self.LSM9DS0_OUT_Z_L_M) | self.mag.readU8(self.LSM9DS0_OUT_Z_H_M) << 8

        magArr = [magX, magY, magZ]

        for i in range(len(magArr)):
            if magArr[i] > 32767:
                magArr[i] -= 65536

        return magArr

    def temperature(self):
        temp = self.mag.readList(self.LSM9DS0_OUT_TEMP_L_XM) | self.mag.readList(self.LSM9DS0_OUT_TEMP_H_XM) << 8

        return temp

    def roll(self):
    	# get roll
        return

    def pitch(self):
    	# get pitch
        return

    def yaw(self):
    	# get yaw
        return

    def dpsX(self):
    	# get degrees per second on X axis
        return

    def dpsY(self):
    	# get degrees per second on Y axis
        return

    def dpsZ(self):
    	# get degrees per second on Z axis
        return

    def filtered(self):
    	# get filtered data
        return self.complementary_filter()

    def complementary_filter(self):
    	# run complementary filter methodology
        PI_F    = math.pi
        orient  = {
            'gyro':     {
                'raw':  self.gyroscope(),
                'dps':  []
            },
            'accel':    {
                'raw':      self.accelerometer(),
                'degrees':  []
            },
            'mag':      {
                'raw':  self.magnetometer()
            },
            'temp':     {
                'raw':  ''
            },
            'filtered':     {
                    'x':    0.0,
                    'y':    0.0,
                    'z':    0.0
                }
        }


        # convert gyro raw to degrees per second
        dpsX    = (orient['gyro']['raw'][0]*self.GYRO_SENSITIVITY)
        dpsY    = (orient['gyro']['raw'][1]*self.GYRO_SENSITIVITY)
        dpsZ    = (orient['gyro']['raw'][2]*self.GYRO_SENSITIVITY)
        orient['gyro']['dps']   = [dpsX,dpsY,dpsZ]

        # track this gyro over time
        self.gyroXangle     += orient['gyro']['dps'][0] * self.DT
        self.gyroYangle     += orient['gyro']['dps'][1] * self.DT
        self.gyroZangle     += orient['gyro']['dps'][2] * self.DT

	# get roll, pitch and yaw
	roll    = ((math.atan2(orient['accel']['raw'][1],orient['accel']['raw'][2])+self.M_PI)*self.RAD_TO_DEG)
	pitch   = ((math.atan2(orient['accel']['raw'][2],orient['accel']['raw'][0])+self.M_PI)*self.RAD_TO_DEG)
	yaw     = (math.atan2(orient['mag']['raw'][2] * math.sin(roll) - orient['mag']['raw'][1] * math.cos(roll), orient['mag']['raw'][0] * math.cos(pitch) + orient['mag']['raw'][1] * math.sin(pitch) * math.sin(roll) + orient['mag']['raw'][2] * math.sin(pitch) * math.cos(roll)))
            
        # convert accelerometer data to degrees
        orient['accel']['degrees']  = [roll,pitch,yaw]

        # run complementary filter (reset current angle)
        self.CFangleX   = 0.98*(self.CFangleX+orient['gyro']['dps'][0]*self.DT)+(0.02*orient['accel']['degrees'][0])
        self.CFangleY   = 0.98*(self.CFangleY+orient['gyro']['dps'][1]*self.DT)+(0.02*orient['accel']['degrees'][1])
	self.CFangleZ   = 0.98*(self.CFangleZ+orient['gyro']['dps'][2]*self.DT)+(0.02*orient['accel']['degrees'][2])

        # set filtered response
        orient['filtered']['x']     = self.CFangleX
        orient['filtered']['y']     = self.CFangleY
        orient['filtered']['z']     = self.CFangleZ

        return orient

    def kalman_filter(self):
    	# run kalman filter methodology
        return



