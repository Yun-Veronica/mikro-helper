#!/bin/bash

# Install Python 3 and pip
apt-get update
apt-get install -y python3 python3-pip

# Install Python dependencies
pip3 install -r requirements.txt

# Copy your Python script and configuration files to appropriate directories
#cp -r /path/to/your/python_script /usr/local/bin/
#cp -r /path/to/your/config.ini /etc/your_app/

# Set permissions and configurations as needed
chmod +x /usr/local/bin/your_script

# Optionally, create a symlink to make your script executable from anywhere
ln -s /usr/local/bin/your_script /usr/bin/your_script

# Clean up
apt-get clean
