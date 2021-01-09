# Test to see if sound sensor code works.

import os
import sys


absolute_path = os.getcwd ()


sys.path.insert (0, "%s/platform"%absolute_path)
sys.path.insert (0, "%s/platform/sensors"%absolute_path)
sys.path.insert (0, "%s/platform/sensors/soundtest"%absolute_path)


from SSM import *


# Not a part of the program.
if ("__main__" == __name__):

	configure_sound_sensor()

	while (True):
		try:
			user_input = input()
			print (gio_status)
			print (get_sound_sensor_gio(17))

		except KeyboardInterrupt:
			print ("")
			exit (0)
