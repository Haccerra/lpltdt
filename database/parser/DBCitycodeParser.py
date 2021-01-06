# Parse database with all city codes.


class DBCitycodeParser:

	# @Brief: Constructor function.
	# @Attrb: dblocation - string where the parsed database is stored.
	#       : debug      - development filed to test if the database is properly parsed.
	# 	: citycodes  - list with the parsed codes.
	# @Throw: TypeError  - values passed to constructor are not as expected.
	def __init__ (self, dblocation, debug = False):
		self.dblocation    = dblocation
		self.debug         = debug
		self.citycodes     = []

		# Verify proper value types.
		if (False == isinstance (self.dblocation, str)):
			raise TypeError ("Argument dblocation of class DBCitycodeParser expected to receive STRING but got %s"%str(dblocation))
		if (False == isinstance (self.debug, bool)):
			raise TypeError ("Argument debug of class DBCitycodeParser expected to receive BOOL but got %s"%str(debug))


	# @Brief: Open the database at the specified path.
	# @Input: None
	# @Retrn: None
	# @Throw: TypeError - incorrect path specified (not a path to database)
	def read(self):
		# Check if the path to database is properly passed (should be handled during development).
		try:
			# Open file in the read mode.
			# File is self-closed after exiting with open statement.
			with open (self.dblocation, "r") as filehandler:
				for fhline in filehandler:
					# Parse the data according to the db rule:
					#	[citycode]	[cityname]
					citycode_start_position = fhline.find ("[")
					citycode_final_position = fhline.find ("]")
					cityname_start_position = fhline.find ("[", citycode_start_position+1)
					cityname_final_position = fhline.find ("]", citycode_final_position+1)

					citycode = fhline[citycode_start_position+1:citycode_final_position]	# Parsed two letter city code.
					cityname = fhline[cityname_start_position+1:cityname_final_position]	# Parsed full city name.

					self.citycodes.append ( [citycode, cityname] )				# Append to database

		except Exception:
			print ("DEV MESSAGE: No database file could be located at %s path."%self.dblocation)
			raise TypeError ("Incorrect argument.")

		# Debug mode requested.
		if (False != self.debug):
			self.__debug_read_function()


	# @Brief: Private method to debug the class functions behaviour.
	# @Input: None
	# @Retrn: None
	# @Throw: None
	def __debug_read_function(self):
		print (100*"*")
		if (0 != len(self.citycodes)):
			for city in self.citycodes:
				citycode, cityname = city
				print (citycode, cityname)
				print("")
		else:
			print ("DEV MESSAGE: An empty list cannot be debugged.")
		print (100*"*")
		print ("")


