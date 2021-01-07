# License Plate Detection algorithm.


# Import license plate detection library.
from openalpr import Alpr as alpr
from vehicleclassifier import VehicleClassifier as alprvc


class Lpltdt:
	
	# @Brief: Class constructor.
	# @Attrb: imsource       - list of all image data provided by CMM module.
	# 	: alpr_result_no - number of results given by ALPR for specific image.
	# 	: alpr_vehicle   - use vehicle classifier.
	#	: alpr_country   - country for which the program is used.
	#	: alpr_config    - location to preinstalled configuration of alpr library. Should be default value if bash omnirun.sh --install has been ran.
	#	: alpr_runtime   - location to preinstalled runtime data  of alpr library. Should be default value if bash omnirun.sh --install has been ran.
	# @Throw: TypeError - incorrect argument format.
	def __init__ (self, imsource, alpr_result_no = 1, alpr_vehicle = False, alpr_country = "eu", alpr_config = "/etc/openalpr/openalpr.conf", alpr_runtime = "/usr/share/openalpr/runtime_data"):

		# Assign values.
		self.imsource     = imsource		# Must always be a list.
		self.alpr_vehicle = alpr_vehicle
		self.alpr_country = alpr_country
		self.alpr_config  = alpr_config
		self.alpr_runtime = alpr_runtime


		# Check for proper types.
		if (False == isinstance (imsource, list):
			raise TypeError ("DEV MESSAGE: Argument imsource of class Lpltdt expected to get a list, but got %s."%str(type(imsource)))
		if (0 == len(imsource)):
			raise TypeError ("DEV MESSAGE: Argument imsource of class Lpltdt cannot be empty.")
		if (False == isinstance (alpr_vehicle, bool)):
			raise TypeError ("DEV MESSAGE: Argument alrp_vehicle of class Lpltdt expected to be bool, but got %s."%str(type(alpr_vehicle)))
		if (False == isinstance (alpr_country, str)):
			raise TypeError ("DEV MESSAGE: Argument alpr_country of class Lpltdt expected to be string, but got %s."%str(type(alpr_country)))
		if (False == isinstance (alpr_config, str)):
			raise TypeError ("DEV MESSAGE: Argument alpr_config of class Lpltdt expected to be string, but got %s."%str(type(alpr_config)))
		if (False == isinstance (alpr_runtime, str)):
			raise TypeError ("DEV MESSAGE: Argument alpr_runtime of class Lpltdt expected to be string, but got %s."%str(type(alpr_runtime)))


		# Create alpr object. Normally, parameters alpr_destination and alpr_runtime should not be changed from the input default values.
		self.alpr = alpr(country, alpr_destination, alpr_runtime)

		# Check if vehicle classifier should be created.
		self.vclass = alprvc(alpr_destination, alpr_runtime)

		# Check if ALPR could be instantialised.
		if (False == self.alpr.is_loaded()):
			raise TypeError ("DEV MESSAGE: ALPR could not be properly instantialised. Most likely alpr_country object is not appropriate.")
		# Check if VehicleClassifier could be instantialised.
		if (False == self.vclass.is_loaded()):
			if (False == self.alpr_vehicle):
				# It was not requested to create vehicle classifier.
				self.vclass = None
			else:
				# It was requested to create vehicle classifier, but the operation failed.
				raise TypeError ("DEV MESSAGE: ALPR VehicleClassifier could not be properly instantialised. Reason unknown.")

		# Check if alpr_result_no argument is actually int.
		if (False == isinstance(alpr_result_no, int)):
			raise TypeError ("DEV MESSAGE: Argument alpr_result_no of class Lpltdt expected to be string, but got %s."%str(type(alpr_result_no)))

		# Set maximum number of results provided by ALPR library.
		self.alpr.set_top_n (alpr_result_no)		#Default value is "1". This is generally the best candidate. More results are not planned to be handled.



	# @Brief: Method to destroy object.
	# @Input: None
	# @Retrn: None
	# @Throw: None
	def selfdestroy (self):
		# Unload ALPR objects from memory.
		if (False != self.alpr.is_loaded()):
			self.alpr.unload()
		if (False != self.vclass.is_loaded()):	
			self.vclass.unload()

		# Remove self.
		del self


	# @Brief: Function to check if license plates could be found in the image.
	# @Input: None
	# @Retrn: implates - list of strings found on processed image.
	# @Throw: None
	def lp_process(self):

		# Method return value.
		implates = []

		for image in imsource:
			alpr_result = self.alpr.recognize_ndarray (image) # Get result from image data passed as numpy array.

			# Check if any plate has been found.
			if (0 != len(alpr_result["results"])):
				for id, plates in enumerate(alpr_result["results"]):
					# First candidate is always candidate with highest probability. There is no planned use for rest of the candidates.
					best_candidate = plates["candidates"][id]					
					implates.append ( [image, best_candidate["plate"], best_candidate["confidence"] )	# Store the image and license plate found data.

					# For loop is used for generic solution, but currently only the best candidate is planned. Functionally same as:
					#	bast_candidate = alpr_result["results"]["candidates"][0]					
					break
			else:
				implates.append ( [None, None, None] )	# Nothing found on the image, therefore the image is irrelevant.

		return implates


	# @Brief: Function to check make and model of the car from an image.
	# @Input: None
	# @Retrn: imcar - list of cars found on a processed image.
	# @Throw: None
	def vehicle_classify(self)		

		# Method return value.
		imcar = []

		if (False != self.alpr_vehicle):
			for image in imsource:
				vehicle_result = self.vclass.recognize_ndarray (image) # Get result from image data passed as numpy array.

				# Find best car candidate.
				best_candidate = None
				for attribute, candidates in vehicle_results.items():
    					for candidate in candidates:
						if ("missing" == candidate["name"])
							imcar.append ( [None, None, None] )
						else:
							imcar.append ( [imcar, attribute, candidate] )

		else:
			raise ValueError ("DEV MESSAGE: Vehicle Classification method from Lpltdt class requested while alpr_vehicle attribute is set to False.")







