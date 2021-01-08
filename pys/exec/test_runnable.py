# Verify algorithm precission on test data images located on local memory drive.


import os
import cv2 as cv
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

	db = dbtest.DBTestdataParser(countryDB, dirDatabase)

	try:
		db.read()
		dbinfo = db.get_db_data()

		for id, carimage in enumerate (dbinfo[CARIMAGE]):
			try:
				image = cv.imread (os.getcwd () + "testdata" + carimage)
				lpalgo = lpltdt.Lpltdt( [image] )
				result = lpalgo.lp_process()

				if (dbinfo[LPLTTEXT][id] == result[0][1]):
					correctly_found_on_car_images = correctly_found_on_car_images + 1
				else:
					incorrectly_found_on_car_images.append (carimage, dbinfo[LPLTTEXT][id], result[0][1])

			except Exception:
				print ("Image on a path %s could not be opened."%(os.getcwd()+"testdata"+carimage))

		for id, pltimage in enumerate (dbinfo[PLTIMAGE]):
			pass

	except Exception:
		print ("Database %s could not be parsed."%countryDB)
		exit (1)


	# Get user command.
	print("Parsing process has been completed.")
	user_command = input ("Enter command to see results (enter help to see list of available options): "

	try:
		while (True):
			if ("help" == user_command):
				pass
			elif ("statistic results" == user_command):
				pass
			elif ("see errors" == user_command):
				pass
			elif ("export results" == user_command):
				pass
			elif ("terminate" == user_command):
				pass
			else
				pass

	except KeyboardException:
		print ("")
		exit (1)



