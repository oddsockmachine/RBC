git clone https://github.com/geringonca/RBC.git
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
pip install -r requirements_rpi.txt
echo ""
echo "python node.py foo"
