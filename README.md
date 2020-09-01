# ONMT Models

Training script for OpenNMT models tested on Ubuntu 20.04 with NVidia Driver 440.100 and GeForce GTX 780. Models available for download [here](https://drive.google.com/drive/folders/11wxM3Ze7NCgOk_tdtRjwet10DmtvFu3i).

Trains an OpenNMT model and a SentencePiece parser then packages them for use with [Argos Translate](https://github.com/argosopentech/argos-translate). 

## Running
- Install NVIDIA drivers
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
sudo docker run --gpus all -it --name cuda -p 6006:6006 nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 bash
```
- Inside Docker container download training script 
```
apt-get install git vim -y
cd /root
git clone https://github.com/argosopentech/onmt-models
```
- Run ```setup.sh``` to install OpenNMT-tf, ctranslate2, and sentencepiece
- Copy training data into onmt-models/raw_data with the source text at raw_data/source.<sl> and the target at raw_data/source.<tl>. Set values for $sl and $tl in config.sh. 
- Run ```train.sh``` to train
- Once SentencePiece has finished training can be stopped with Ctrl-C and resumed with ```resume_train.sh```
- Run ```package.sh``` to convert to a CTranslate model and package model for [Argos Translate](https://github.com/argosopentech/argos-translate). The packaged model will be at <sl>_<tl>.argosmodel
- If you want to delete all of the generated files but not your source files run ```reset.sh```. You will lose any model training progress.
- To copy the model out of the docker container and into your host system *from your host system* run:
```
sudo docker cp cuda:/root/<sl>_<tl>.argos_model
```
- Packages also need a [NLTK Punkt](https://www.nltk.org/api/nltk.tokenize.html#module-nltk.tokenize.punkt) model called ```punkt.pickle``` in its root for sentence boundary detection. Pretrained NLTK pickles are available for a number of European Languages from [NLTK](https://www.nltk.org/data.html). Once you have the appropriate pickle for your source language unzip the .argosmodel file, rename the pickle to  ```punkt.pickle``` in the root of the package, and rezip it.
- Packages also need a metadata.json in the root as defined in argos-translate/argos_translate/package.py
- REAME.md files can optionally also be put in the root directory.

### Batch Size
Depending on your GPU you may want to tweak ```batch_size``` in ```config.yml```. This works with a GPU with 2GB or GPU memory. If you have more memory increasing the batch size should give you better performance. If you have a less powerful GPU you may need to decrease batch size for this script to run.

### Data
Parallel Corpuses for training are available [here](https://drive.google.com/drive/folders/1E_JMvYzP5wLGSF0wAulYNc5xGQHkVrDR?usp=sharing), these are a combination of several [Opus](http://opus.nlpl.eu/) corpuses.
 
