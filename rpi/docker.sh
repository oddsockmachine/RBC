wget https://download.docker.com/linux/raspbian/dists/stretch/pool/stable/armhf/docker-ce_17.12.1~ce-0~raspbian_armhf.deb
sudo apt install libltdl7
sudo dpkg -i ./docker-ce_17.12.1~ce-0~raspbian_armhf.deb
sudo docker run hello-world
