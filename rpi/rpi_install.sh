vcgencmd display_power 0
sudo apt-get install htop tree
sudo apt-get install build-essential libssl-dev libffi-dev python3-dev
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-venv
sudo apt-get install python3-gpiozero
cd RBC
pyvenv venv
source venv/bin/activate
which pip
which python
python -V
sudo pip3 install RPi.GPIO
pip install -r requirements_rpi.txt
echo ""
echo "python node.py foo"


cd ~/docker-rpi-nodered
sudo docker run --rm -it -p 1880:1880 -v ~/node-red-data:/data --name mynodered nodered/node-red-docker:rpi

tail -f /var/log/homeassistant/home-assistant.log

cd ~/RBC/cfg_mgr
db_host=localhost python3 cfg_mgr.py

cd ~/RBC/DB
sudo docker-compose up

postgraphile -c postgres://postgres:mysecretpassword@localhost/postgres -n 0.0.0.0 -w
