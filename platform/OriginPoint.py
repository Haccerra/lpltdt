# !/env/bin/python3
# Connect Device to Wolkabout platform.

# Libraries
import sys


# Get arguments provided by omnirun.sh script.
try:
	absolute_path = sys.argv[1]
	user_command  = sys.argv[2]
except Exception:
	print("ABORT: Please start the program by executing omnirun.sh script!")
	exit(1)


# Add program subdirectories to interpreter path.
sys.path.insert (0, "%s/platform"%absolute_path)
sys.path.insert (0, "%s/platform/connectivity"%absolute_path)
sys.path.insert (0, "%s/platform/sensors"%absolute_path)


# Additional custom libraries needed for program to work.
from IoT import IoT


# OriginPoint.py is the entry point of the program. No other python executed script must start the program.
if ("__main__" == __name__):
	pass
else:
	print ("ABORT: Module platform/main.py must be directly executed!")
	exit(1)


# Starting point of the program
if ("--start" == user_command):
	RPi = IoT()
	RPi.establish_connection()

elif ("--quit" == user_command):
	try:
		RPi.cancel_connection()
	except:
		print ("ABORT: Something went wrong. Program will stop execution now.")
		exit(1)
	exit(0)

elif ("help" == user_command):
	print ("Program options: ")
	print ("\t --start")
	print ("\t --quit")

else:
	pass



