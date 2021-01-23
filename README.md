# ONMT Models

Trains an OpenNMT model and a SentencePiece parser then packages them with a Stanza model for use with [Argos Translate](https://github.com/argosopentech/argos-translate). 

Argos Translate packages available for download [here](https://drive.google.com/drive/folders/11wxM3Ze7NCgOk_tdtRjwet10DmtvFu3i). OpenNMT checkpoints with SentencePiece files available for download at [https://drive.google.com/drive/folders/1fE7I4QD_W5Ul_CQzBHppE17wd-KQ_XPq](https://drive.google.com/drive/folders/1fE7I4QD_W5Ul_CQzBHppE17wd-KQ_XPq).

## Data
Uses data from the [Opus project](http://opus.nlpl.eu/) in the Moses format.

## Running
- Install NVIDIA drivers
- You may need to add additional swap space
```
sudo fallocate -l 75G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show
```
- Install Docker:
```
sudo apt-get update && sudo apt-get install docker.io
```
- Install [NVIDIA Container Toolkit](https://github.com/NVIDIA/nvidia-docker):
```
# Add the package repositories
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```
- Start Docker container 
```
sudo docker run --gpus all -it --name cuda -p 6006:6006 nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu20.04 bash
```
- Inside Docker container download training script 
```
apt-get install git vim zip -y
cd /root
git clone https://github.com/argosopentech/onmt-models
```
- Run ```setup.sh``` to install OpenNMT-tf, ctranslate2, and sentencepiece
- Copy training data into onmt-models/raw_data with the source text at raw_data/source.<sl> and the target at raw_data/source.<tl>. Set values for $sl and $tl in config.sh and config.yml. 
- Run ```train.sh``` to train
- Once SentencePiece has finished model training can be stopped with Ctrl-C and resumed with ```resume_train.sh```
- Optionally edit ```metadata.json``` and ```MODEL_README.md``` which will be packaged with your model
- Run ```package.sh``` to convert to a CTranslate model and package model for [Argos Translate](https://github.com/argosopentech/argos-translate). The packaged model will be at <sl>_<tl>.argosmodel
- If you want to delete all of the generated files but not your source files run ```reset.sh```. You will lose any model training progress.
- To copy the model out of the docker container and into your host system *from your host system* run:
```
sudo docker cp cuda:/root/onmt-models/<sl>_<tl>.argosmodel .
```
- Run ```export_checkpoint.sh``` to export a zip archive of your averaged OpenNMT checkpoints and files for sentencepiece tokenization. ```reset_packaging.sh``` deletes everything generated while packaging, but unlike ```reset.sh``` leaves your trained models intact.

