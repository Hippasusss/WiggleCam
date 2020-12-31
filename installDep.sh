sudo apt-get update -y; sudo apt-get upgrade -y;

sudo apt-get install python3-opencv python3-pip -y; pip3 install vidgear opencv-python picamera;

sudo raspi-config nonint do_camera 0;
