# Verify algorithm precission on test data images located on local memory drive.


import os
import cv2 as cv
import Lpltdt as lpltdt
import DBTestdataParser as dbtest


# @Brief:
# @Input: dirDatabase - program absolute path to database directory.
#	: countryDB   - database to be parsed.
# @Retrn: None
# @Throw: None
def testflow(dirDatabase, countryDB):

	correctly_found_on_car_images = 0
	correctly_found_on_plt_images = 0

	incorrectly_found_on_car_images = []
	incorrectly_found_on_plt_images = []

	try:
		db = dbtest.DBTestdataParser(countryDB, dirDatabase)

	except Exception:
		print ("DEV MESSAGE: Failed to create db object inside test_runnable.py script.")

	try:
		db.read()
		dbinfo = db.get_db_data()

		try:
			for _, carimage in enumerate (dbinfo):
				image = cv.imread ("testdata" + carimage[dbtest.CARIMAGE])
				lpalgo = lpltdt.Lpltdt ([image])
				result = lpalgo.lp_process()

				if (carimage[dbtest.LPLTTEXT] == result[0][1]):
					correctly_found_on_car_images = correctly_found_on_car_images + 1
				else:
					incorrectly_found_on_car_images.append ([carimage[dbtest.CARIMAGE], carimage[dbtest.LPLTTEXT], result[0][1]])

			for _, pltimage in enumerate (dbinfo):
				image = cv.imread ("testdata" + pltimage[dbtest.PLTIMAGE])
				lpalgo = lpltdt.Lpltdt ([image])
				result = lpalgo.lp_process()

				if (carimage[dbtest.LPLTTEXT] == result[0][1]):
					correctly_found_on_plt_images = correctly_found_on_plt_images + 1
				else:
					incorrectly_found_on_plt_images.append ([pltimage[dbtest.PLTIMAGE], pltimage[dbtest.LPLTTEXT], result[0][1]])

		except Exception:
			print ("Cannot open an image.")
			exit (1)

	except Exception:
		print ("Database %s could not be parsed."%(dirDatabase + countryDB))
		exit (1)


	# Get user command.
	print("Parsing process has been completed.")

	try:
		while (True):
			user_command = input ("Enter command to see results (enter help to see list of available options): ")

			if ("help" == user_command):
				print ("")
				print (100*"*")
				print ("Next commands are available:")
				print ("\tstatistic results :: tells about how many license plates were properly classified.")
				print ("\tsee errors        :: shows only the images where improper data were found.")
				print ("\texport results    :: export all results to a log file.")
				print ("\tterminate test    :: terminates program test execution.")
				print (100*"*")
				print ("\n")

			elif ("statistic results" == user_command):
				statistic_results(						\
							countryDB, 				\
							correctly_found_on_car_images, 		\
							correctly_found_on_plt_images, 		\
							incorrectly_found_on_car_images, 	\
							incorrectly_found_on_plt_images		\
						 )

			elif ("see errors" == user_command):
				see_errors(countryDB, incorrectly_found_on_car_images, incorrectly_found_on_plt_images)

			elif ("export results" == user_command):
				export_to_file(								\
							os.getcwd () + "/logs/dev/" + countryDB,	\
							incorrectly_found_on_car_images,		\
							incorrectly_found_on_plt_images			\
					      )

			elif ("terminate test" == user_command):
				print("")
				exit (0)

			else:
				pass

	except KeyboardInterrupt:
		print ("")
		exit (1)


# @Brief: Output results performed from test command.
# @Input: country          - testdata used for country.
#	: correct_car_im   - number of correctly processed data from car images.
#	: correct_plt_im   - number of correctly processed data from plt images.
#	: incorrect_car_im - list of incorrectly processed data from car images.
#	: incorrect_plt_im - list of incorrectly processed data from plt images.
# @Retrn: None
# @Throw: None
def statistic_results(country, correct_car_im, correct_plt_im, incorrect_car_im, incorrect_plt_im):
	
	# Calculate number of images used.
	number_of_car_images = correct_car_im + len (incorrect_car_im)
	number_of_plt_images = correct_plt_im + len (incorrect_plt_im)
	# Calculate percentage.
	correctly_evaluated_lp_on_car_images = float (float (correct_car_im / number_of_car_images) * 100)
	correctly_evaluated_lp_on_plt_images = float (float (correct_plt_im / number_of_plt_images) * 100)

	print ("")
	print (100*"*")
	print (100*"*")
	print ("Results from testing %s license plate from testdata is following:"%country)
	print ("\tProperly classified license plates from images with car: %s"%str (correctly_evaluated_lp_on_car_images)+"%")
	print ("\tProperly classified license plates from images with plt: %s"%str (correctly_evaluated_lp_on_plt_images)+"%")
	print ("\t"+100*"*")
	print ("\tWhen classifing license plates on images with car total of %s/%s were properly classified."%(str(correct_car_im), str(number_of_car_images)))
	print ("\tWhen classifing license plates on images with plt total of %s/%s were properly classified."%(str(correct_plt_im), str(number_of_plt_images)))
	print ("\t"+100*"*")
	print ("\tTotal percentage number of license plates improperly classified using car images: %s"%str(float(100)-correctly_evaluated_lp_on_car_images)+"%")
	print ("\tTotal percentage number of license plates improperly classified using plt images: %s"%str(float(100)-correctly_evaluated_lp_on_plt_images)+"%")
	print (100*"*")
	print (100*"*")
	print ("")


# @Brief: Display on which images errors were found.
# @Input: country          - testdata used for country.
#	: incorrect_car_im - data about incorrectly evaluated testdata.
#	: incorrect_plt_im - data about incorrectly evaluated testdata.
# @Retrn: None
# @Throw: None
def see_errors(country, incorrect_car_im, incorrect_plt_im):

	print ("")
	print (100*"*")
	print (100*"*")
	print ("Next car images were improperly classified for %s country: "%country)
	if (0 == len (incorrect_car_im)):
		print ("\tNONE.")
	else:
		for data in incorrect_car_im:
			print ("\tOn image: %s expected %s, but got %s."%(data[0], data[1],data[2]))

	print (100*"*")
	print ("Next plt images were improperly classified for %s country: "%country)
	if (0 == len (incorrect_plt_im)):
		print ("\tNONE.")
	else:
		for data in incorrect_plt_im:
			print ("\tOn image: %s expected %s, but got %s."%(data[0], data[1], data[2]))
	
	print (100*"*")
	print (100*"*")
	print ("")


# @Brief:
# @Input: filename - name of country for which logging was used.
#	: incorrect_car_im - data with improperly processed license plates on car images.
#	: incorrect_plt_im - data with improperly processed license plates on plt images.
# @Retrn: None
# @Throw
def export_to_file(filename, incorrect_car_im, incorrect_plt_im):

	with open (filename + "car-img.md", "w") as filehandler:
		for data in incorrect_car_im:
			filehandler.write (			\
				"""

				CAR IMAGE:  %s
				CAR PLATE:  %s
				CAR DETECT: %s

				""" 				\
				% (data[0], data[1], data[2])	\
			)

	with open (filename + "plt-img.md", "w") as filehandler:
		for data in incorrect_plt_im:

			filehandler.write (			\
				"""

				CAR IMAGE:  %s
				CAR PLATE:  %s
				CAR DETECT: %s

				""" 				\
				% (data[0], data[1], data[2])	\
			)


