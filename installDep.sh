sudo apt-get update -y; sudo apt-get upgrade -y;

sudo apt-get install python3-opencv python3-pip -y; 
pip3 install vidgear opencv-python picamera;

pip3 install opencv-contrib-python; 
sudo apt-get install -y libatlas-base-dev libhdf5-dev libhdf5-serial-dev libatlas-base-dev libjasper-dev  libqtgui4  libqt4-test;

sudo raspi-config nonint do_camera 0;
