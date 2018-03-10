wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key

sudo apt-key add mosquitto-repo.gpg.key

cd /etc/apt/sources.list.d/

sudo wget http://repo.mosquitto.org/debian/mosquitto-wheezy.list

sudo apt-get update

sudo apt-get install mosquitto

sudo apt-get install mosquitto-clients

sudo cp mosquitto.conf /etc/mosquitto/mosquitto.conf

sudo /etc/init.d/mosquitto restart

