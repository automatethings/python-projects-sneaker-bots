# http://invent.module143.com/daskal_tutorial/rpi-3-tutorial-13-wireless-pi-to-pi-python-communication-with-nrf24l01/
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24 
import time
import spidev
import json

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

pipes 	= [
	[0xe7,0xe7,0xe7,0xe7,0xe7],
	[0xc2,0xc2,0xc2,0xc2,0xc2]
]

radio 	= NRF24(GPIO,spidev.SpiDev())
radio.begin(0,17)	# address/pin?
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_2MBPS)
radio.setPALevel(NRF24.PA_MIN)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

# radio.openReadingPipe(1,pipes[1])
radio.openWritingPipe(pipes[1])
radio.printDetails()

# radio.startListening()
# message = list(input("Enter a message to send: "))
try:
	counter = 0
	while True:
		counter 	+= 1
		msg 		= "counter: {}".format(counter)
		msg 		= {'sensor': 'light','lux': counter}

		# convert dict to JSON (string)
		msg 		= json.dumps(msg)

		# convert JSON to binary
		#binary 		= ' '.join(format(ord(letter), 'b') for letter in msg)

		#print binary
		#binary  	= "Hello World: {}".format(counter)

		# convert JSON into string
		binary 		= str(msg)

		# must be of type list or int 
		message 	= list(binary)
		radio.write(message)
		print "We sent the message of {}".format(message)

		# check if it returned ack payload
		if radio.isAckPayloadAvailable():
				returnedPL 	= []
				radio.read(returnedPL,radio.getDynamicPayloadSize())
				print "Our returned pauload was {}".format(returnedPL)
		else:
			print "No payload received"

		time.sleep(1)
except KeyboardInterrupt:
	print 'keyboard interruption'
except Exception as e:
	print 'caught exception'
	print e
finally:
	GPIO.cleanup()