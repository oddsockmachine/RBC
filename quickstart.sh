git clone https://github.com/oddsockmachine/RBC.git

sudo apt-get update
sudo apt install tree
python3 -V
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
# sudo dpkg-reconfigure locales
cd RBC/nodule
pyvenv venv
source venv/bin/activate
which python
which pip
python --version
pip install -r requirements/requirements.txt
# python nodule.py


sudo vim /etc/network/interfaces
auto wlan0
iface wlan0 inet dhcp
wpa-ssid <Your Access Point Name aka SSID>
wpa-psk <Your WPA Password>

sudo ifup wlan0


sudo nmtui
sudo ifconfig wlan0
sudo iwconfig wlan0

sudo armbianmonitor -m
