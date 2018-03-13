http://lucsmall.com/2017/01/19/beginners-guide-to-the-orange-pi-zero/

sudo apt-get update

sudo dpkg-reconfigure tzdata

sudo vim /etc/network/interfaces

 auto wlan0
 iface wlan0 inet dhcp
 wpa-ssid <Your Access Point Name aka SSID>
 wpa-psk <Your WPA Password>

