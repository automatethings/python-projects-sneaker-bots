import LSM9DS0

# create LSM9DS0 instance
sensor 	= LSM9DS0.LSM9DS0(1)

# init 3d cube
#cube 	= CUBE.3D()
# init chart(s)


while True:
	# grab LSM9DS0 data
	data 	= sensor.filtered()
	print(data)

	# update 3d cube
	# update line chart(s)