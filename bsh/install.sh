# !/bin/bash

# Script which installs all the necessary libraries for openALPR to work.
# Creates a system variable alpr which can be accessed in shell scripts.

# Prerequisites.
sudo apt-get install -y openalpr openalpr-daemon openalpr-utils libopenalpr-dev
sudo apt-get install -y libopencv-dev libtesseract-dev git cmake build-essential libleptonica-dev
sudo apt-get install -y liblog4cplus-dev libcurl3-dev

# For openalpr-daemon.
sudo apt-get install -y beanstalkd

# Download library.
git clone https://github.com/openalpr/openalpr.git

# Create build source directory.
cd openalpr/src
mkdir build
cd build

# Make compile environment.
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr -DCMAKE_INSTALL_SYSCONFDIR:PATH=/etc ..

# Compile library.
make

# Install library.
sudo make install

# Remove library data created during installation process.
rm -rf openalpr
