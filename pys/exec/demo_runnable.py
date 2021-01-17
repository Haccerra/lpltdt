# Demonstrate how algorithm works using testdata.


import os
import datetime
import cv2 as cv
import numpy as np
import CMM as cmm
import Lpltdt as lpltdt
import DBResidentEditor as dbresidents


# @Brief: Demonstrate algorithm basic operation.
# @Input: None
# @Retrn: None
# @Throw: None
def demoflow():

	# Create objects.
	camera = cmm.CMM()
	lpalgo = lpltdt.Lpltdt([None])

	# Work objects.
	image = []

	# Fetch user input and decide what to show based on it.
	while (True):

		try:
			user_command = input("Input the demo command. To see more information enter help: ")

			if ("help" == user_command):
				print (100*"*")
				print ("Enter one of the following commands:")
				print ("\tcaptimg :: take an image from camera.")
				print ("\tcaptvid :: take series of images from camera.")
				print ("\tprocess :: try to find license plates on an image.")
				print ("\timgshow :: preview image taken by the camera.")
				print ("\timgtest :: path to test image (does not take an image from camera but from memory drive).")
				print ("\tdemoesc :: abort the program execution.")
				print (100*"*")
				print ("\n")

			elif ("captimg" == user_command):
				# Clear image list
				image = []

				camera.set_recording_mode(cmm.STILL_IMAGE_MODE)
				image.append (np.asarray (camera.capture_still_image())) 

			elif ("captvid" == user_command):
				# Clear image list
				image = []

				camera.set_recording_mode(cmm.LIVE_IMAGE_MODE)
				image.append (camera.record_video())

			elif ("process" == user_command):
				db = dbresidents.DBResidentEditor(os.getcwd () + "/database/residents.db")

				try:
					data = db.read()

				except Exception:
					print ("DEV MESSAGE: Could not open the database at %s path."%(os.getcwd () + "/database/residents.db"))
					os.exit (1)

				if (0 != len(image)):

					try:
						lpalgo.set_new_image_source(image)
						result = lpalgo.lp_process()

						belongs_to_resident = False
						for entry in data:
							if (entry[dbresidents.RESIDENT_CAR_LICENSE] == result[0][1]):
								print ("\033[1m\033[36mLOG: \033[93m%s:%s:%s \033[91m%s %s\033[0m entered the garage (car data: \033[1m\033[95m%s %s %s\033[0m)" 	\
									%(									\
										datetime.datetime.now ().hour,					\
										datetime.datetime.now ().minute,				\
										datetime.datetime.now ().second,				\
										entry[dbresidents.RESIDENT_NAME],				\
										entry[dbresidents.RESIDENT_SURNAME],				\
										entry[dbresidents.RESIDENT_CAR_BRAND],				\
										entry[dbresidents.RESIDENT_CAR_MODEL],				\
										entry[dbresidents.RESIDENT_CAR_LICENSE]				\
									 )									\
								      )
								belongs_to_resident = True

						if (False == belongs_to_resident):
							print ("\033[1m\033[91mNo resident could be found with\033[93m %s \033[91mlicense plate registration.\033[0m"%result[0][1])


					except Exception:
						print ("Could not process the bufferred image.")

				# Remove image buffer.
				image = []

			elif ("imgshow" == user_command):
				if (0 != len(image)):

					try:
						for im in image:
							cv.imshow ("imgshow", cv.rotate(im, cv.ROTATE_180))
							cv.waitKey (0)
					except Exception:
						print ("No image could be shown.")

			elif ("imgtest" == user_command):
				impath = input ("Enter path to an image: ")

				try:
					image_test = cv.imread (os.getcwd() + "/" + impath)
					image.append (image_test)
				except Exception:
					print ("Image does not exist on specified path")

			elif ("demoesc" == user_command):
				print ("")
				exit (0)

			else:
				pass

		except KeyboardInterrupt:
			print ("")
			exit (0)


