# Parse database with all test image dataset information.


# Literal fields for proper sublist information handling provided from the class.
CARIMAGE = 0
PLTIMAGE = 1
LPLTTEXT = 2


class DBTestdataParser:

	# @Brief: Constructor function for the class.
	# @Attrb: dblocation - path to database to be parsed.
	# 	: program_absolute_path - absolute path to the program
	#	: debug - activates debug during development.
	# @Throw: TypeError - incorrect argument types passed to constructor.
	def __init__ (self, dblocation, program_absolute_path, debug = False):
		self.debug                 = debug
		self.dblocation            = dblocation
		self.program_absolute_path = program_absolute_path
		self.dbinformation         = []

		# Verify datatypes passed to constructor. If incorrect, raise an error.
		if (False == isinstance (self.debug, bool)):
			raise TypeError ("Argument debug of class DBTestdataParser expected BOOL, but got %s"%str(debug))
		if (False == isinstance (self.dblocation, str)):		# Python with version < 3.0 uses basestring instead of str. Not a problem if everything is executed through omnirun.sh.
			raise TypeError ("Argument dblocation of class DBTestdataParser expected STRING, but got %s"%str(dblocation))
		if (False == isinstance (self.program_absolute_path, str)):
			raise TypeError ("Argument program_absolute_path of clas DBTestdataParser expected STRING, but got %s"%str(program_absolute_path))


	# @Brief: Open and parse database with test image data.
	# @Input: None
	# @Retrn: None
	# @Throw: TypeError - path to database incorrect.
	def read(self):
		beginblock = False
		finalblock = False

		# Try to open database. If it exists, parse the database according to rule:
		# BEGIN TEST DATA BLOCK
		# 	image_license_plate_path=data_to_be_parsed
		#	image_vehicle_plate_path=data_to_be_parsed
		#	image_license_plate_text=data_to_be_parsed
		# END TEST DATA BLOCK
		try:
			# Open database to be parsed.
			with open (self.dblocation, "r") as filehandler:
				temporary_data = []	# store parsing results.

				for fhline in filehandler:
					# Parse the information as long as it belongs to the block.
					if (False != beginblock):
						search_for_eq_sign = fhline.find ("=")
						if (-1 != search_for_eq_sign):	# EqSign found.
							temporary_data.append (fhline[search_for_eq_sign+1:-1])	# copy either of the three parameter data which are of interest.

					# Check if begin/end block syntax has been found.
					if   (-1 != fhline.find ("BEGIN TEST DATA BLOCK")): # Key syntax found.
						beginblock = True
						finalblock = False

					elif (-1 != fhline.find ("END TEST DATA BLOCK")):   # Key syntax found.
						beginblock = False
						finalblock = True
					else:
						pass

					# End block syntax found. Copy temporary data to the class attribute list.
					if (False != finalblock):
						carimage, pltimage, lplttext = temporary_data

						# Add the temporary stored data to object attribute.
						self.dbinformation.append ([							\
										(self.program_absolute_path + carimage),	\
										(self.program_absolute_path + pltimage),	\
										(lplttext)					\
									  ])

						# Free memory and reinstantialise the empty list.
						del temporary_data
						temporary_data = []

						# Reset flag.
						finalblock = False

			if (False != self.debug):
				self.__debug_read_function()
							
		except Exception:
			print ("DEV MESSAGE: No database file could be located at %s path."%self.dblocation)
			raise TypeError ("Incorrect argument.")


	# @Brief: Local function for debug information.
	# @Input: None
	# @Retrn: None
	# @Throw: None
	def __debug_read_function(self):
		print (100*"*")
		if (0 == len (self.dbinformation)):
			print ("DEV MESSAGE: Nothing could be parsed.")
		else:
			for info in self.dbinformation:
				carimage, pltimage, lplttext = info
				print (carimage, pltimage, lplttext)
				print("")
		print (100*"*")
		print ("")


	# @Brief: Return parsed data obtained by read method.
	# @Input: None
	# @Retrn: self.dbinformation
	# @Throw: None
	def get_db_data(self):
		return self.dbinformation

