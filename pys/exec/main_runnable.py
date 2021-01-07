# Branching to start the requested program control flow.


# @Brief: Main control flow branch.
# @Input: program_absolute_path - absolute path location propagated from omnirun.sh script.
#	: program_database_absolute_path - databases for citycodes and testdata.
#	: user_requested_mode - information propagated from omnirun.sh script.
# @Retrn: None
# @Throw: None
def controlflow(program_absolute_path, program_database_absolute_path, user_requested_mode):
	if ("--start" == user_requested_mode):
		pass
	elif ("--calib" == user_requested_mode):
		pass
	elif ("--demo" == user_requested_mode):
		pass
	else:
		print ("Argument %s is not defined. Check the available program start option arguments by using --help command."%user_requested_mode)
		exit(1)
