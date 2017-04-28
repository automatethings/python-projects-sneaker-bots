import PhotoBooth
import threading

booth 	= PhotoBooth.PhotoBooth()

try:

	# start thread array
	'''
	threads 	= [
		threading.Thread(
			name	= "Booth",
			target	= booth.sleep()
		),
		threading.Thread(
			name	= "Camera",
			target	= booth.live()
		)
	]


	for t in threads:
		t.start()
	'''

	#threading.Thread(target=booth.live(), args=()).start()
	threading.Thread(target=booth.sleep(), args=()).start()

except KeyboardInterrupt:
	print('KEYBOARD INTERRUPT\n')
except Exception as e:
	print(e)
finally:
	print('thanks for using our photo booth!')
	booth.destroy()