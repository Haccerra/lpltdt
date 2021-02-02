# !/bin/bash

# Used to install all pip dependencies.

sudo pip3 install openalpr
sudo pip3 install opencv-python
sudo pip3 install Pillow

# Additional libraries for opencv.
sudo apt-get install -y libatlas-base-dev libjasper-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev libqtgui4 libqt4-test 
sudo apt-get install -y libilmbase-dev libopenexr-dev libgstreamer1.0-dev libavcodec-dev libavformat-dev libswscale-dev libwebp-dev

# GUI library.
sudo apt-get install -y python3-tk
sudo pip3 install tk

# Wolkabout.
python3 -m pip install wolk-connect==3.1.0

