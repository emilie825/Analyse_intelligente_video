sudo apt update -y
sudo apt install apt-transport-https ca-certificates curl gnupg2 software-properties-common y
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" -y
sudo apt update -y
apt-cache policy docker-ce -y
sudo apt install docker-ce -y
sudo curl -L https://github.com/docker/compose/releases/download/1.24.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose -y
sudo chmod +x /usr/local/bin/docker-compose -y
sudo apt-get install python python-pip -y
curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
sudo apt-get install build-essential nodejs -y
sudo npm install forever -y