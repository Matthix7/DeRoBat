#!/bin/bash

# If needed : chmod +x ~/launch.sh
# To launch : nohup ~/launch.sh

cd ~/Documents/DeRoBat/Sonar
./Test_devices &
sleep 2
cd ~/Documents/DeRoBat/Communication
python3 Client.py &
sleep 2

# To stop : sudo killall Test_devices python3
