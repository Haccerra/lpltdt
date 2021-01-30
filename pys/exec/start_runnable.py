# Program logic.


import os
import sys
import time
import threading
import datetime
import cv2 as cv
import IoT as wolkabout
import CMM as cmm
import SSM as ssm
import Lpltdt as lpltdt
import DBResidentEditor as dbresidents


illegal_access_id = 1
list_of_residents_already_in_building = []


# @Brief: Function where the algorithm for program to work is stored.
# @Input: program_absolute_path - string with information about absolute path to program execution directory.
#	: program_database_absolute_path - string with information about absolute path to databases usedd by the program.
# @Retrn: None
# @Throw: None
def workflow(program_absolute_path, program_database_absolute_path):

	global illegal_access_id
	global list_of_residents_already_in_building

	# Connect to IoT platform.
	iot_connection = wolkabout.IoT()
	iot_connection.establish_connection(config = program_absolute_path)

	# Create work objects.
	camera = cmm.CMM(image_rotation = 180)
	lpalgo = lpltdt.Lpltdt([ None ])

	try:

		ssm.configure_sound_sensor()

		while (True):
			# Eazy way to eliminate long honking sounds.
			time.sleep (10)

			# Start taking camera images.
			if (cmm.STILL_IMAGE_MODE == camera.get_recording_mode()):
				while (ssm.get_sound_sensor_gio()):
					pass						# Wait untill sound sensor reacts.

				#time.sleep (camera.get_capture_timer())		# Delay capturing new image untill requested time passes. Sleep preferred to active threading.
				lstImageData = camera.capture_still_image()
			else:
				while (ssm.get_sound_sensor_gio()):
					pass

				lstImageData = camera.record_video()

			# Try to find license plate.
			if (False == lstImageData.any()):
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
					found_status = check_if_resident_found_in_db(lstAlgoResult[0][1])

					if (0 != len(found_status)):
						# Write resident to table.
						resident_status = []
						for id, resident in enumerate (list_of_residents_already_in_building):
							if (resident == lstAlgoResult[0][1]):
								resident_status.append ([True, id])

						if (0 != len (resident_status)):
							if (False != resident_status[0][0]):
								list_of_residents_already_in_building.remove (resident_status[0][1])		# Resident left the building.
							else:
								list_of_residents_already_in_building.append (lstAlgoResult[0][1])		# Resident entered the building.

						print ("Access allowed for %s resident."%lstAlgoResult[0][1])				# Print license plates.

						# Create directory for a specific resident using Apartment_NameSurname (if it does not exist already).
						try:
							resident_directory = "savedata/%s_%s%s" %(found_status[0][9], found_status[0][7], found_status[0][8])
							os.mkdir ("%s" %resident_directory)

						except OSError as error:
							pass		# Directory already exists.

						finally:

							# Create directory for specific day where all images from that day will be stored for a given resident.
							try:
								current_day = "%s_%s_%s" %(found_status[0][1], found_status[0][2], found_status[0][3])
								os.mkdir ("%s/%s" %(resident_directory, current_day))

							except OSError as error:
								pass	# Directory already exists.

							finally:
								# Create an image.
								imname = "%s:%s:%s.jpg" %(found_status[0][4], found_status[0][5], found_status[0][6])
								impath = "%s/%s/%s" %(resident_directory, current_day, imname)

								if (cmm.STILL_IMAGE_MODE == camera.get_recording_mode()):
									cv.imwrite ("%s"%impath, lstImageData)		# Still image mode only records a single element (not a list).
								else:
									cv.imwrite ("%s"%impath, lstImageData[0])	# First image from a video.


						# Send information to IoT platform.
						iot_connection.send_camera_readings( 				\
							tplTime     = (						\
									found_status[0][1],			\
									found_status[0][2],			\
									found_status[0][3],			\
									found_status[0][4],			\
									found_status[0][5],			\
									found_status[0][6],			\
								      ),					\
							tplResident = (						\
									found_status[0][7],			\
									found_status[0][8],			\
									found_status[0][9]			\
								      )						\
						)
						iot_connection.send_sound_readings(				\
							tplTime     = (						\
									found_status[0][1],			\
									found_status[0][2],			\
									found_status[0][3],			\
									found_status[0][4],			\
									found_status[0][5],			\
									found_status[0][6],			\
								      ),					\
							imname      = impath					\
						)

					else:
						if (None != lstAlgoResult[0][1]):
							print ("Illegal entry for %s license plates. Access prohibited."%lstAlgoResult[0][1])

							# Save image.
							impath = "savedata/illegal/%s.jpg" %(str(illegal_access_id))

							if (cmm.STILL_IMAGE_MODE == camera.get_recording_mode()):
								cv.imwrite ("%s"%impath, lstImageData)		# Still image mode only records a single element (not a list).
							else:
								cv.imwrite ("%s"%impath, lstImageData[0])	# First image from a video.

							illegal_access_id = illegal_access_id + 1

							# Send data to cloud.
							iot_connection.send_sound_readings_illegal_access (		\
								tplTime = (						\
										datetime.datetime.now ().day,		\
										datetime.datetime.now ().month,		\
										datetime.datetime.now ().year,		\
										datetime.datetime.now ().hour,		\
										datetime.datetime.now ().minute,	\
										datetime.datetime.now ().second,	\
									  ),						\
								lplt    = lstAlgoResult[0][1],				\
								imname  = impath					\
							)


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

		print ("MSG: Program will now close!")
		exit (0)


# @Brief: Check if found license plates belong to any resident.
# @Input: lp_candidate - license plate found by algo.
# @Retrn: resident_found_status - flag which returns all residents data (if found).
# @Throw: None
def check_if_resident_found_in_db(lp_candidate):

	# Return function value.
	resident_found_status = []

	# Try to open residents database.
	db = dbresidents.DBResidentEditor(os.getcwd () + "/database/residents.db")

	try:
		data = db.read()

	except Exception:
		print ("DEV MESSAGE: Could not open the database at %s path."%(os.getcwd () + "/database/residents.db"))
		os.exit (1)

	# Parse the entries in database.
	for entry in data:
		if (entry[dbresidents.RESIDENT_CAR_LICENSE] == lp_candidate):
			resident_found_status.append ([				\
				True,						\
				datetime.datetime.now ().day,			\
				datetime.datetime.now ().month,			\
				datetime.datetime.now ().year,			\
				datetime.datetime.now ().hour,			\
				datetime.datetime.now ().minute,		\
				datetime.datetime.now ().second,		\
				entry[dbresidents.RESIDENT_NAME],		\
				entry[dbresidents.RESIDENT_SURNAME],		\
				entry[dbresidents.RESIDENT_APARTMENT],		\
				entry[dbresidents.RESIDENT_CAR_BRAND],		\
				entry[dbresidents.RESIDENT_CAR_MODEL],		\
				entry[dbresidents.RESIDENT_CAR_LICENSE]		\
			])

	return resident_found_status



