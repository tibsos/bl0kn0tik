#!/bin/bash

# chmod +x ./path_to_script
# ./path_to_script


# Install requirements
echo "Time for me to install the requirements! >:)"
echo " "

echo "Installing Pyhton"
sudo apt-get install python3.8
echo "Python installed"
echo " "

echo "Installing NGINX"
sudo apt-get install nginx
echo "I've NGINX"
echo " "

echo "Installing Django requirements"
pip3 install requirements.txt
echo "I've installed Django requirements"
echo " "
echo "All requirements are installed! ez"

# Run the server

