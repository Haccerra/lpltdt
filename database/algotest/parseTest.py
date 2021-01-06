# Test basic functionality of DB parsing algorithms.

import sys

# Get absolute path of the program via the script call argument.
absolute_program_path = sys.argv[1]

# Insert path to classes which are being tested.
sys.path.insert (0, "%s/database/parser"%absolute_program_path)

# Import tested classes.
import DBCitycodeParser as dbcc
import DBTestdataParser as dbtc


# Since this is just a development debug, this script can only be executed from the outside folder to check if the algorithms are working properly.
# Must be executed directly by calling:
#	python3.7 algotest/parseTest.py absolute_program_location
# To get absolute_program_location, navigate to root of the program and enter pwd in terminal.
if ("__main__" == __name__):
	dbcc_obj = dbcc.DBCitycodeParser("serbia-citycode.db", True)
	dbtc_obj = dbtc.DBTestdataParser("serbia-testdata.db", absolute_program_path, True)

	dbcc_obj.read()
	dbtc_obj.read()
