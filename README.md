# onmt-models
Training script for OpenNMT models tested on Ubuntu 20.04 with NVidia Driver 440.100 and GeForce GTX 780

- Install NVIDIA drivers
- Install Docker

	sudo apt-get update && sudo apt-get install docker.io

- Install [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker)

	# Add the package repositories
	distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
	curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
	curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

	sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
	sudo systemctl restart docker


- Start Docker container 

	sudo docker run --gpus all -it --name cuda -p 6006:6006 nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 bash

- Inside Docker container download training script 

	apt-get install git vim -y
	git clone https://github.com/argosopentech/onmt-models

- Run setup.sh to install OpenNMT-tf, ctranslate2, and sentencepiece
- Copy training data into onmt-models/raw_data and update location in the top of train.sh
- Run train.sh to train
- Once SentencePiece has finished training can be stopped with Ctrl-C and resumed with resume_train.sh
- 
