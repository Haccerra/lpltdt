# Camera Management Module


# Library for connecting and executing commands by RPi camera module.
import picamera
import picamera.array
import time
import numpy as np
import cv2   as cv


# Possible values for recording mode argument of the class.
STILL_IMAGE_MODE = 0
LIVE_IMAGE_MODE  = 1


class CMM:

	# @Brief: Class constructor of Camera Management Module.
	# @Attrb: tplResolution  - (width, height) of number of pixels provided by the camera (camera resolution).
	# 	: image_rotation - angle by which camera image should be rotated (to compensate improper montage).
	#	: recording_mode - decide if seperate pictures will be taken after N seconds, or license plates will be searched on video (X FPS).
	#	: capture_timer  - in first case detailed in recording_mode, defines number of seconds which need to pass before snipping a new image.
	#	: FPS            - framerate in second case for recording_mode (video used).
	#	: debug          - used for development purpose.
	# @Throw:
	def __init__ (self, tplResolution = (640, 480), image_rotation = 0, recording_mode = STILL_IMAGE_MODE, capture_timer = 5, FPS = 5, debug = False):

		# Assign values to attributes.
		self.camera = picamera.PiCamera()			# PiCamera object module.
		self.timer  = 0						# timer which holds the number of seconds passed.
		try:
			# Possibility that tplResolution cannot be unpacked because tuple was expected.
			self.pixelcount_width  = tplResolution[0]	# pixel width of camera
			self.pixelcount_height = tplResolution[1]	# pixel height of camera
		except Exception:
			raise TypeError ("DEV MESSAGE: Argument tplResolution of class CMM expected to be tupple of 2 integer numbers but got %s."%str(tplResolution))

		self.image_rotation    = image_rotation			# rotate input image by image_rotation deg.
		self.recording_mode    = recording_mode			# use still frame capture or video mode
		self.capture_timer     = capture_timer			# number of seconds between which a still image is captured.
		self.FPS               = FPS				# number of frames used in video capturing.
		self.debug             = debug

		# Check if argument types are appropriate.
		if (False == isinstance (tplResolution, tuple)):
			raise TypeError ("DEV MESSAGE: Argument tplResolution of class CMM expected to be a tupple, but got %s."%str(type(tplResolution)))
		if (2 != len(tplResolution)):
			raise TypeError ("DEV MESSAGE: Argument tplResolution of class CMM expected to have 2 elements, but got %s."%str(len(tplResolution)))
		if (False == isinstance (self.pixelcount_width, int)):
			raise TypeError ("DEV MESSAGE: Argument tplResolution[0] for pixelcount_width for class CMM expected to be int, but got %s."%str(self.pixelcount_width))
		if (False == isinstance (self.pixelcount_height, int)):
			raise TypeError ("DEV MESSAGE: Argument tplResolution[1] for pixelcount_height for class CMM expected to be int, but got %s."%str(self.pixelcount_height))
		if (False == isinstance (image_rotation, int)):
			raise TypeError ("DEV MESSAGE: Argument image_rotation of calss CMM expected to be int, but got %s."%str(image_rotation))
		if ((-360 > image_rotation) or (360 < image_rotation)):
			raise TypeError ("DEV MESSAGE: Argument image_rotation of class CMM expected to be in range [-360, 360], but got %s."%str(image_rotation))
		if (False == isinstance (recording_mode, int)):
			raise TypeError ("DEV MESSAGE: Argument recording_mode of class CMM expected to be int, but got %s."%str(recording_mode))
		if ((STILL_IMAGE_MODE != recording_mode) and (LIVE_IMAGE_MODE != recording_mode)):
			raise TypeError ("DEV MESSAGE: Argument recording_mode of class CMM expected to have either STILL_IMAGE_MODE(0) or LIVE_IMAGE_MODE(1) values, but got %s."%str(recording_mode))
		if (False == isinstance (capture_timer, int)):
			raise TypeError ("DEV MESSAGE: Argument capture_timer of class CMM expected to be int, but got %s."%str(capture_timer))
		if (False == isinstance (FPS, int)):
			raise TypeError ("DEV MESSAGE: Argument FPS of class CMM expected to be int, but got %s."%str(FPS))
		if (False == isinstance (debug, bool)):
			raise TypeError ("DEV MESSAGE: Argument debug of class CMM expected to be bool, but got %s."%str(debug))


		# Initialise camera settings.
		self.camera.resolution = (self.pixelcount_width, self.pixelcount_height)

		if (STILL_IMAGE_MODE == recording_mode):
			pass
		else:
			self.camera.framerate = self.FPS


	# @Brief: Function to capture an image every N seconds.
	# @Input: None
	# @Retrn: image - array of w,h data obtained from camera.
	# @Throw: ValueError - method called with improper recording_mode set.
	def capture_still_image(self):
		# Method return value.
		image = None

		# Method must be threaded.
		if (STILL_IMAGE_MODE == self.recording_mode):

			# Create rawdata object.
			rawdata = picamera.array.PiRGBArray(self.camera, size = self.camera.resolution)
			# Make small time window for camera to get ready.
			time.sleep (0.25)	# 250ms.

			# Fetch the stored data from the camera module.
			self.camera.capture(rawdata, format = "bgr")	# BGR is legacy format of openCV library used by openALPR.
			image = rawdata.array

			# Rotate the image if needed.
			if (0 != self.image_rotation):
				if (+180 == abs(self.image_rotation)):
					image = cv.rotate (image, cv.ROTATE_180)
				if (-90  == self.image_rotation):
					image = cv.rotate (image, cv.ROTATE_90_COUNTERCLOCKWISE)
				if (+90  == self.image_rotation):
					image = cv.rotate (image, cv.ROTATE_90)

			return image

		else:
			raise ValueError ("DEV MESSAGE: Argument recording_mode of CMM class set to LIVE_IMAGE_MODE, but method capture_still_image was requested.")


	# @Brief: Function to record video with X framerate.
	# @Input: None
	# @Retrn: image_array - array of w,h array data (multiple images).
	# @Throw: VaueError - method called with improper recording_mode set.
	def record_video(self):
		# Method return value.
		image_array = []

		if (LIVE_IMAGE_MODE == self.recording_mode):

			# Create rawdata object.
			rawdata = picamera.array.PiRGBArray(self.camera, size = self.camera.resolution)
			# Make small time window for camera to get ready.
			time.sleep (0.25)	# 250ms.

			# Process frame by frame.
			number_of_frames_captured = 0

			for frame in self.camera.capture_continuous(rawdata, format = "bgr", use_video_port = True):

				image = frame.array			# Get image data

				# Rotate the image, if needed.
				if (0 != self.image_rotation):
					if (+180 == abs(self.image_rotation)):
						image = cv.rotate (image, cv.ROTATE_180)
					if (-90  == self.image_rotation):
						image = cv.rotate (image, cv.ROTATE_90_COUNTERCLOCKWISE)
					if (+90  == self.image_rotation):
						image = cv.rotate (image, cv.ROTATE_90)

				image_array.append (image)		# Store new frame.
				rawdata.truncate(0)			# Clear streamed data.

				# Handle max number of frames.
				number_of_frames_captured = number_of_frames_captured + 1

				if (number_of_frames_captured >= self.FPS):
					break				# Ready to return camera data to control flow program to process and see if there are any license plate on the snipped frames.

			return image_array

		else:
			raise ValueError ("DEV MESSAGE: Argument recording_mode of CMM class set to STILL_IMAGE_MODE, but method record_video was requested.")


	# @Brief: Set function for self.recording_mode field.
	# @Input: recording_mode - new value for recording_mode argument.
	# @Retrn: None
	# @Throw: None
	def set_recording_mode(self, recording_mode):
		self.recording_mode = recording_mode


	# @Brief: Return capture_time which was set for this object. Needs to properly thread capture_still_image method.
	# @Input: None
	# @Retrn: self.capture_timer
	# @Throw: None
	def get_capture_timer(self):
		return self.capture_timer


	# @Brief: Return recording_mode in order to know which of the methods (for still image or video) can be used by the program.
	# @Input: None
	# @Retrn: self.recording_mode
	# @Throw: None
	def get_recording_mode(self):
		return self.recording_mode

