# !/bin/bash
# Shell script to start the program properly.

# Absolute program path.
PWD2SCRIPT=$(dirname $(readlink -f $0))
# User command.
USERCMD=$1

if [[ --install == $USERCMD ]]
then
	if [[ $LPLTDT ]]
	then
		echo "********************************************************************************************************"
		echo Install process already completed. New request will be rejected.
		echo In case --install process must be triggered again do the following:
		echo -e "\t" unset LPLTDT
		echo -e "\t" bash omnirun.sh --install
		echo "********************************************************************************************************"
	else
		echo "********************************************************************************************************"
		echo Program will now install all dependencies. This process will take a while.
	
		# System dependencies.
		sudo apt-get install -y python3.7
	
		# Install openALPR library (which will install all the dependencies - openCV, tesseract, leptonica).	
		bash $PWD2SCRIPT/bsh/install.sh
		# Remove library data created during installation process.
		rm -rf openalpr

		# Python dependencies.
		python3 -m pip install wolk-connect
		bash $PWD2SCRIPT/bsh/camera-install.sh
		bash $PWD2SCRIPT/bsh/pypip.sh

		echo Installation process completed.
		echo "********************************************************************************************************"

		# Create a system variable to know install process has been completed.
		export LPLTDT
		export LC_ALL=C		# Remove !strcmp(locale, "C") error.
	fi

elif [[ --setup == $USERCMD ]]
then
	echo "********************************************************************************************************"
	bash $PWD2SCRIPT/bsh/alias.sh
	. ~/.bashrc
	echo lpltdt alias configured.
	echo "********************************************************************************************************"

elif [[ --editor == $USERCMD ]]
then
	# Start resident database editing program.
	chmod +x $PWD2SCRIPT/pys/residenteditor.py
	python3 $PWD2SCRIPT/pys/residenteditor.py $PWD2SCRIPT $2
	chmod -x $PWD2SCRIPT/pys/residenteditor.py

elif [[ --help == $USERCMD ]]
then
	echo "********************************************************************************************************"
	echo Welcome to LPLTDT program. To use the program, following [OPTION] are applicable:"\n"
	echo -e "\t" --install "\t" sets up the environment needed for program to work";"
	echo -e "\t" --remove  "\t" removes all the packages installed through --install process";"
	echo -e "\t" --destroy "\t" completely removes all files from the project";"
	echo -e "\t" --memfree "\t" removes testdata to save the space on drive.
	echo -e "\t" --setup   "\t" optional step which adds lpltdt alias to be used instead of bash omnirun.sh command";"
	echo -e "\t" --start   "\t" start the program";"
	echo -e "\t" --calib   "\t" allows program parameters to be calibrated to change program behaviour in an easy way";"
	echo -e "\t" --editor  "\t" start resident editor subprogram";"
	echo -e "\t" --demo    "\t" presentation mode enabled. "\n\n"
	echo To run the program execute omnirun.sh script in either of the two following ways:
	echo -e "\t" bash omnirun.sh [OPTION]
	echo or by executing:
	echo -e "\t" chmod +x omnirun.sh
	echo -e "\t" ./omnirun.sh [OPTION] "\n\n"
	echo In case --setup has been performed, lpltdt alias will exist in environment. It can be checked by typing:
	echo -e "\t" alias
	echo -e in terminal. "\n\n"
	echo Then, program can be executed in following way:
	echo -e "\t" lpltdt [OPTION]
	echo "********************************************************************************************************"

else
	# Start program.
	chmod +x $PWD2SCRIPT/platform/OriginPoint.py
	python3.7 $PWD2SCRIPT/platform/OriginPoint.py $PWD2SCRIPT $USERCMD
	chmod -x $PWD2SCRIPT/platform/OriginPoint.py
fi
