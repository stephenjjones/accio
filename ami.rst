Documentation on how the base AMI was configured
------------------------------------------------

**This is for reference only and does not need to be run by the end user**

Install docker CE

https://docs.docker.com/install/linux/docker-ce/ubuntu/#set-up-the-repository

sudo apt-get update

sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install docker-ce

sudo docker run hello-world

sudo apt-get install build-essential

sudo apt-get install linux-headers-$(uname -r)

Install the CUDA toolkit
# https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1604&target_type=debnetwork

wget http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-repo-ubuntu1604_9.1.85-1_amd64.deb

sudo dpkg -i cuda-repo-ubuntu1604_9.1.85-1_amd64.deb
sudo apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub

sudo apt-get update

sudo apt-get install cuda

Install nvidia-docker https://github.com/NVIDIA/nvidia-docker#xenial-x86_64
$ curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | \
  sudo apt-key add -

$ curl -s -L https://nvidia.github.io/nvidia-docker/ubuntu16.04/amd64/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

$ sudo apt-get update

$ sudo apt-get install -y nvidia-docker2

$ sudo pkill -SIGHUP dockerd

$ docker run --runtime=nvidia --rm nvidia/cuda nvidia-smi

Enable running docker without sudo:
https://docs.docker.com/install/linux/linux-postinstall/
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
$ newgrp docker
