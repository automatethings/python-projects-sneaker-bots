# http://invent.module143.com/daskal_tutorial/rpi-3-tutorial-13-wireless-pi-to-pi-python-communication-with-nrf24l01/
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24 
import time
import spidev

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

radio.openReadingPipe(1,pipes[0])
radio.openWritingPipe(pipes[1])
radio.printDetails()

# radio.startListening()

def receivedData():
	print "Ready to receive data"
	radio.startListening()

	while not radio.available(0):
		time.sleep(1/100)

	receivedMessage 	= []
	radio.read(receivedMessage,radio.getDynamicPayloadSize())

	print "Translating receivedMessage to unicode characters"
	string 	= ""
	for n in receivedMessage:
		# decode into standard unicode set
		if (n >= 32 and n <=126):
			string += chr(n)
	print "Our slave sent us {}".format(string)
	radio.stopListening()


try:
	while True:
		command 	= "GET_TEMP"
		message 	= list(command)
		# message 	= list("Hello World")
		radio.write(message)
		print "We sent the message of {}".format(message)

		# Check if it returned ackPL
		if radio.isAckPayloadAvailable():
			returnedPL 	= []
			radio.read(returnedPL,radio.getDynamicPayloadSize())
			print "Our returned payload was {}".format(returnedPL)
			receivedData()
		else:
			print "No payload received"
		time.sleep(1)
except KeyboardInterrupt:
	print 'keyboard interruption'
except:
	print 'caught exception'
finally:
	GPIO.cleanup()