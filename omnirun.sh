# !/bin/bash
# Shell script to start the program properly.

# Absolute program path.
PWD2SCRIPT=$(dirname $(readlink -f $0))
# User command.
USERCMD=$1

if [[ --install == $USERCMD ]]
then
	# System dependencies.
	sudo apt-get install -y python3.7
	
	# Install openALPR library (which will install all the dependencies - openCV, tesseract, leptonica).
	sh install.sh

	# Python dependencies.
	python3 -m pip install wolk-connect

else
	# Start program.
	chmod +x $PWD2SCRIPT/platform/OriginPoint.py
	python3.7 $PWD2SCRIPT/platform/OriginPoint.py $PWD2SCRIPT $USERCMD
	chmod -x $PWD2SCRIPT/platform/OriginPoint.py
fi
