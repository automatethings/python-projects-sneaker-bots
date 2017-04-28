# import
import cv2
import time
import sys
import PIL
from PIL import Image
from PIL import ImageOps
import os
import os.path
import threading

class PhotoBooth:

	def __init__(self):

		# setup audio (depending on system)
		self.audio 		= 'afplay'

		# setup display
		#self.rows 		= 4 	# len(self.sequence) now defines this
		self.columns 	= 2
		self.width 		= 600
		self.height 	= 900

		# setup sequence
		# TODO: for now we're assuming 4 sequence (it matters for height/width of our print strip)
		self.sequence 	= [
			{
				'before': 	'wav/sequence-1-before.wav',
				'after': 	''
			},
			{
				'before': 	'wav/sequence-2-before.wav',
				'after': 	''
			},
			{
				'before': 	'wav/sequence-3-before.wav',
				'after': 	''
			},
			{
				'before': 	'wav/sequence-4-before.wav',
				'after': 	'wav/goodbye.wav'
			},
		]

		# setup camera & strip to display
		self.camera 	= cv2.VideoCapture(0)
		self.strip 		= Image.new('RGB', (self.width, self.height), (255,255,255))

	def start(self):
		# play welcome message
		os.system('%s wav/welcome.wav' % self.audio)

		# begin sequence
		cnt=0
		for wav in self.sequence:
			# TODO: validate sequence input

			# play before wav
			if os.path.exists(wav['before']):
				os.system('%s %s' % (self.audio,wav['before']))

			# take snapshot
			self.snapshot(cnt)
			cnt+=1

			# play after wav
			if os.path.exists(wav['after']):
				os.system('%s %s' % (self.audio,wav['after']))

			time.sleep(0.5)

		# display the strip 
		# TODO: print the strip
		self.display()

		# lets sleep again
		self.sleep()

	def snapshot(self,row):
		if self.strip:
			# Grab an image from the webcam.
			image 	= self.img()

			# determine desired width and height
			height 	= (self.height - ((len(self.sequence)+1) * 15)) / len(self.sequence)
			width 	= (self.width - ((self.columns - 1) * 10)) / self.columns

			# Scale/crop the image to fit our desired width/height.
			image 	= ImageOps.fit(image, (width, height), PIL.Image.LANCZOS)

			y = (row * height) + ((row+1) * 15)

			for column in xrange(self.columns):
			  x = (column * width) + (column * 10)
			  grayscale 	= (0,1)
			  # Check if this column should be grayscaled.
			  if grayscale[column]:
			    self.strip.paste(ImageOps.grayscale(image), (x, y))
			  else:
			    self.strip.paste(image, (x, y))

	def img(self):
		retval, image = self.camera.read()
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = Image.fromarray(image)
		return image

	def display(self):
		if self.strip:
			self.strip.show()

	def sleep(self):
		raw_input('press any key to start')
		self.start()

	def live(self):
		print('starting live')
		while self.camera.isOpened():
			retval, frame 	= self.camera.read()
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			# Display the resulting frame
			cv2.imshow('Live Feed',gray)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

	def destroy(self):
		self.camera.release()
		cv2.destroyAllWindows()