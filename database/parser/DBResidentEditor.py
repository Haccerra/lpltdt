# Class to edit information about residents.


# Literals used for parsed data
RESIDENT_NAME        = 0
RESIDENT_SURNAME     = 1
RESIDENT_APARTMENT   = 2
RESIDENT_CAR_BRAND   = 3
RESIDENT_CAR_MODEL   = 4
RESIDENT_CAR_LICENSE = 5


class DBResidentEditor:

	# @Brief: Constructor function.
	# @Attrb: database_location - string with location to resident.db
	# @Throw: TypeError - impropriate argument types passed
	def __init__ (self, database_location):

		# Assign values.
		self.database_location = database_location

		# Check if types are appropriate
		if (False == isinstance (database_location, str)):
			raise TypeError ("DEV MESSAGE: Argument database_location of class DBResidentEditor expected STRING, but got %s."%str(type(database_location)))


	# @Brief: Open a database and return all necessary information.
	# @Input: None
	# @Retrn: dbdata - list with values relevant to all residents.
	# @Throw: ValueError - impossible to open requested database.
	def read(self):

		# Function return value.
		dbdata = []
		# Temporary data values.
		tempdata = []

		begin_parse = False
		end_parse = False

		try:
			with open (self.database_location, "r") as filehandler:
				for line in filehandler:
					if (False != begin_parse):
						find_eq_sign = line.find("=")

						if (-1 != find_eq_sign):
							tempdata.append (line[find_eq_sign+1:-1])

					if (-1 != line.find ("BEGIN NEW RESIDENT DATA BLOCK")):
						begin_parse = True
						end_parse = False
					elif (-1 != line.find ("END NEW RESIDENT DATA BLOCK")):
						begin_parse = False
						end_parse = True
					else:
						pass

					if (False != end_parse):
						end_parse = False

						dbdata.append (tempdata)
						tempdata = []

		except:
			raise ValueError ("ABORT: Database could not be located at %s path."%self.database_location)

		return dbdata


	# @Brief: Add new resident in database.
	# @Input: dbentry - list with all data needed for resident to be added.
	# @Retrn: None
	# @Throw: TypeError - incorrect argument format passed.
	#	: ValueError - impossible to open requested database.
	def append(self, dbentry):

		if (False == isinstance (dbentry, list)):
			raise TypeError ("DEV MESSAGE: Argument dbentry of method append from class DBResidentEditor expected a list, but got: %s."%str(type(dbentry)))
		if (6 != len (dbentry)):
			raise TypeError ("DEV MESSAGE: Argument dbentry of method append from class DBResidentEditor expected 6 elements (name, surname, apartment, brand, model, license), but got %s."%str(len(dbentry)))

		try:
			with open (self.database_location, "a") as filehandler:

				# Create new entry.
				data = \
				"""

				BEGIN NEW RESIDENT DATA BLOCK
				\tresident_name=%s
				\tresident_surname=%s
				\tresident_apartment=%s
				\tresident_car_brand=%s
				\tresident_car_model=%s
				\tresident_car_license=%s
				END NEW RESIDENT DATA BLOCK

				""" \
				% (dbentry[RESIDENT_NAME], dbentry[RESIDENT_SURNAME], dbentry[RESIDENT_APARTMENT], dbentry[RESIDENT_CAR_BRAND], dbentry[RESIDENT_CAR_MODEL], dbentry[RESIDENT_CAR_LICENSE])

				# Write to a file.
				filehandler.write (data)

		except Exception:
			raise ValueError ("ABORT: Database could not be located at %s path."%self.database_location)



	# @Brief: Remove specific entry based on license plates (because this field is surely unique).
	# @Input: license_plates - string with license plates to be removed.
	# @Retrn: None
	# @Throw: ValueError
	def remove(self, license_plates):

		try:
			remember_line = None
			filedata = None

			with open (self.database_location, "r") as filehandler:
				filedata = filehandler.readlines()

				for id, line in enumerate (filedata):
					if (-1 != line.find ("resident_car_license=%s"%license_plates)):
						# This block must be removed.
						remember_line = id
						break

			# License plates exist. Resident can be removed.
			if (None != remember_line):
				skip_lines_lst = [ remember_line-6, remember_line-5, remember_line-4, remember_line-3, remember_line-2, remember_line-1, remember_line, remember_line+1 ]

				with open (self.database_location, "w") as filehandler:
					for id, line in enumerate (filedata):
						skip = False

						for remove in skip_lines_lst:
							if (id == remove):
								skip = True

						if (False == skip):
							filehandler.write (line)

		except Exception:
			raise ValueError ("ABORT: Database could not be located at %s path."%self.database_location)


	# @Brief: Remove all database information.
	# @Input: None
	# @Retrn: None
	# @Throw: ValueError - impossible to open requested database.
	def cleanup(self):
		try:
			with open (self.database_location, "w") as filehandler:
				pass

		except Exception:
			raise ValueError ("ABORT: Database could not be located at %s path."%self.database_location)
		

