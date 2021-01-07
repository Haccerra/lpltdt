# !/env/bin/python3
# Connect Device to Wolkabout platform.

# Libraries
import sys


# Get arguments provided by omnirun.sh script.
try:
	absolute_path = sys.argv[1]
	user_command  = sys.argv[2]
except Exception:
	print("ABORT: Please start the program by executing omnirun.sh script! For more information use bash omnirun.sh --help to see list of control options.")
	exit(1)


# Add program subdirectories to interpreter path.
sys.path.insert (0, "%s/platform"%absolute_path)
sys.path.insert (0, "%s/platform/connectivity"%absolute_path)
sys.path.insert (0, "%s/platform/sensors"%absolute_path)
sys.path.insert (0, "%s/database/parser"%absolute_path)
sys.path.insert (0, "%s/pys"%absolute_path)
sys.path.insert (0, "%s/pys/exec"%absolute_path)


# Set aboslute path of database files.
database_files_location = "%s/database/"%absolute_path


# Additional custom libraries needed for program to work.
from main_runnable import controlflow


# OriginPoint.py is the entry point of the program. No other python executed script must start the program.
if ("__main__" == __name__):
	controlflow(				 \
			absolute_path,		 \
			database_files_location, \
			user_command		 \
		   )
else:
	print ("ABORT: Module platform/main.py must be directly executed!")
	exit(1)



