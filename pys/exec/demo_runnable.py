# Demonstrate how algorithm works using testdata.


import os
import cv2 as cv
import CMM as cmm
import Lpltdt as lpltdt


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
				image.append (camera.capture_still_image())

			elif ("captvid" == user_command):
				# Clear image list
				image = []

				camera.set_recording_mode(cmm.LIVE_IMAGE_MODE)
				image.append (camera.record_video())

			elif ("process" == user_command):
				if (0 != len(image)):

					try:
						lpalgo.set_new_image_source(image)
						result = lpalgo.lp_process()

						print (result[0][1])

					except Exception:
						print ("Could not process the bufferred image.")

				# Remove image buffer.
				image = []

			elif ("imgshow" == user_command):
				if (0 != len(image)):

					try:
						for im in image:
							cv.imshow ("imgshow", im)
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


