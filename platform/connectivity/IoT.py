# !/env/bin/python3
# Connect to wolk platform.

# Libraries
import wolk


# Varibles
from SecurityInfo import SECURITY_KEY, SECURITY_PASSWORD


# Device status values used to distinguish whether connection has been established.
DEVICE_CONNECTED    = 0
DEVICE_DISCONNECTED = 1


# Class used to establish connection between RPi and IoT platform.
class IoT:

	# @Brief: Class constructor
	# @Attrb: connectivity_status - argument which represents if the connection with the IoT platform has been established.
	# 	: platform_key        - argument with key value generated by IoT platform.
	#       : platform_password   - argument with password value generated by IoT platform.
	#       : device              - argument of WolkConnect object type
	def __init__(self, host = "iot-elektronika.ftn.uns.ac.rs", port = 1883):
		self.connectivity_status = DEVICE_DISCONNECTED
		self.platform_key        = SECURITY_KEY
		self.platform_password   = SECURITY_PASSWORD
		self.device              = None
		self.host                = host
		self.port                = port


	# @Brief: Make a connection between RPi and Wolkabout.
	# @Input: None
	# @Retrn: None
	# @Throw: None
	def establish_connection(self):
		# Establish connection and store the data.		
		self.device = wolk.WolkConnect (												\
						    device = wolk.Device (key = self.platform_key, password = self.platform_password),		\
						    host = self.host,										\
						    port = self.port										\
					       )
		self.device.connect()


	# @Brief: Disconnect RPi from Wolkabout platform.
	# @Input: None
	# @Retrn: None
	# @Throw: ValueError - incorrect value for self.device due to sequence error.
	def cancel_connection(self):
		# Disconnect the device and store the data.
		if (None != self.device):
			self.device.disconnect()
		else:
			raise ValueError ("WARNING: Request to disconnect from the platform given prior to connection request.")


	# @Brief: Log the message that a resident entered the building.
	# @Input: tplTime - information about day, month, year and hours, minutes, seconds.
	#	: tplResident - basic information about the resident (name, surname and which apartment).
	# @Retrn: None
	# @Throw: Exception - method requested prior to connection with cloud.
	def send_camera_readings(self, tplTime, tplResident):

		# Create logging data.
		log_data = 											\
		"""
		Garage access entry:  %s/%s/%s at %s:%s:%s.
		Resident information: %s %s from %s apartment.
		"""												\
			%(											\
				tplTime[0], tplTime[1], tplTime[2], tplTime[3], tplTime[4], tplTime[5],		\
				tplResident[0], tplResident[1], tplResident[2]					\
			)

		# Device must exist.
		if (None != self.device):
			self.device.add_sensor_reading ("CAM", log_data)			# Send data to cloud.
			self.device.publish ()

		else:
			raise Exception ("Improper sequence. Device not connected.")


	# @Brief: Send information to sound sensor on cloud.
	# @Input: tplData - contains data regarding day, month, year, hours, minutes, seconds.
	#	: imname  - name under which an image has been recorded.
	# @Retrn: None
	# @Throw: Exception - method requested prior to connection with cloud.
	def send_sound_readings(self, tplTime, imname):

		# Create logging data.
		log_data = 											\
		"""
		Sensor triggered at: %s/%s/%s at %s:%s:%s.
		Camera recorded  im: %s.
		"""
			%(											\
				tplTime[0], tplTime[1], tplTime[2], tplTime[3], tplTime[4], tplTime[5], 	\
				imname										\
			)

		# Device must exist.
		if (None != self.device):
			self.device.add_sensor_reading ("SOUND", log_data)			# Send data to cloud.
			self.device.publish ()

		else:
			raise Exception ("Improper sequence. Device not connected.")


	# @Brief: Publish information about illegal access request.
	# @Input: tplTime - information about day, month, year, hours, minutes, seconds.
	# 	: lplt - license plates found by algorithm.
	# 	: imname - location to the image.
	# @Retrn: None
	# @Throw: Exception - method requested prior to connection with cloud.
	def send_sound_readings_illegal_access(self, tplTime, lplt, imname):

		# Create logging data.
		log_data =											\
		"""
		Illegal registry recorded at:  %s/%s/%s at %s:%s:%s.
		Camera recorded license plate: %s.
		Camera recorded path of image: %s.
		"""
			%(											\
				tplTime[0], tplTime[1], tplTime[2], tplTime[3], tplTime[4], tplTime[5],		\
				lplt,										\
				imname,										\
			)

		# Device must exist.
		if (None != self.device):
			self.device.add_sensor_reading ("SOUND", log_data)
			self.device.publish ()

		else:
			raise Exception ("Improper sequence. Device not connected.")



