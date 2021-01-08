# Program logic.


import sys
import time
import threading
import IoT as wolkabout
import CMM as cmm
import Lpltdt as lpltdt


# @Brief: Function where the algorithm for program to work is stored.
# @Input: program_absolute_path - string with information about absolute path to program execution directory.
#	: program_database_absolute_path - string with information about absolute path to databases usedd by the program.
# @Retrn: None
# @Throw: None
def workflow(program_absolute_path, program_database_absolute_path):

	# Connect to IoT platform.
	iot_connection = wolkabout.IoT()
	#iot_connection.establish_connection()

	# Create work objects.
	camera = cmm.CMM()
	lpalgo = lpltdt.Lpltdt([ None ])

	try:
		while (True):
			# Start taking camera images.
			if (cmm.STILL_IMAGE_MODE == camera.get_recording_mode()):
				time.sleep (camera.get_capture_timer())			# Delay capturing new image untill requested time passes. Sleep preferred to active threading.
				lstImageData = camera.capture_still_image()
			else:
				lstImageData = camera.record_video()

			# Try to find license plate.
			if (lstImageData.any()):
				pass		# No image has been captured.
			else:
				if (False == isinstance (lstImageData, list)):
					lpalgo.set_new_image_source([lstImageData])	# List must be passed as an argument.
				else:
					lpalgo.set_new_image_source(lstImageData)	# List already provided.
				lstAlgoResult = lpalgo.lp_process()

				if (0 == len(lstAlgoResult)):
					pass						# No license plates have been found.
				else:
					print (lstAlgoResult[0][1])			# Print license plates.

			# Try to do vehicle classification (if set).
			"""
			if (False != lpalgo.get_is_vehicle_classification_set()):
				# Use vehicle classification.
				lstVehicleData = lpalgo.vehicle_classify()

				if (0 == len(lstVehicleData)):
					pass						# No information about the car could be found.
				else:
					print (lstVehicleData[0], lstVehicleData[1], lstVehicleData[2])
			else:
				# Do not use vehicle classificationa algorithm.
				pass
			"""


	# CTRL + C used to terminate program execution.
	except KeyboardInterrupt:

		# Disconnect device from the platform.
		iot_connection.cancel_connection()

		print ("MSG: Program will not close!")
		exit (0)
