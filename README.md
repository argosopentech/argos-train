* Currently porting from Tensorflow to PyTorch and not stable. If you need stable training scripts use this commit: https://github.com/argosopentech/onmt-models/tree/6572085dad0a25698dfc6379820f103833c20190


# ONMT Models

Trains an OpenNMT model and a SentencePiece parser then packages them with a Stanza model for use with [Argos Translate](https://github.com/argosopentech/argos-translate). 

Argos Translate packages available for download [here](https://drive.google.com/drive/folders/11wxM3Ze7NCgOk_tdtRjwet10DmtvFu3i). Legacy OpenNMT-tf checkpoints with SentencePiece files available for download [here](https://drive.google.com/drive/folders/1fE7I4QD_W5Ul_CQzBHppE17wd-KQ_XPq).

## Data
Uses data from the [Opus project](http://opus.nlpl.eu/) in the Moses format.

## Environment
This is the setup currently used to train models:
- NVIDIA Tesla K80 GPU
- 7 cores, 30GB Memory
- Ubuntu 20.04

## Install CUDA
```
curl https://raw.githubusercontent.com/PJ-Finlay/cuda-setup/main/setup.sh | sh
sudo reboot

```

## Install OpenNMT-py
```
cd
git clone https://github.com/OpenNMT/OpenNMT-py.git
cd OpenNMT-py
pip3 install -e .
pip3 install -r requirements.opt.txt
PATH=~/.local/bin:$PATH

```

## Download data
```
cd
git clone https://github.com/argosopentech/onmt-models.git
cd ~/onmt-models/raw_data
wget https://object.pouta.csc.fi/OPUS-Wikipedia/v1.0/moses/en-es.txt.zip
unzip en-es.txt.zip
cat *.en >> source.en
cat *.es >> source.es

```

## Add swap space
```
sudo fallocate -l 75G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show

```

## Install training dependencies
```
cd ~/onmt-models
sudo ./setup.sh

```

## Run training
```
./train.sh

```

# Average checkpoints
./../OpenNMT-py/tools/average_models.py -m <m1> <m2> -o averaged.pt


## More
- Edit config.sh to specify training metadata
- Once SentencePiece has finished model training can be stopped with Ctrl-C and resumed with ```resume_train.sh```
- Optionally edit ```metadata.json``` and ```MODEL_README.md``` which will be packaged with your model
- Run ```package.sh``` to convert to a CTranslate model and package model for [Argos Translate](https://github.com/argosopentech/argos-translate). The packaged model will be at <sl>_<tl>.argosmodel
- If you want to delete all of the generated files but not your source files run ```reset.sh```. You will lose any model training progress.
- To copy the model out of the docker container and into your host system *from your host system* run:
```
sudo docker cp cuda:/root/onmt-models/<sl>_<tl>.argosmodel .
```
- Run ```export_checkpoint.sh``` to export a zip archive of your averaged OpenNMT checkpoints and files for sentencepiece tokenization. ```reset_packaging.sh``` deletes everything generated while packaging, but unlike ```reset.sh``` leaves your trained models intact.
- Screen can be useful to train models on a remote server without maintaining a ssh connection. `screen` to start, `Ctrl-A d` to detach, and `screen -r` to re-attach/

# Troubleshooting
- If you're running out of GPU memory reduce `batch_size` in `config.yml`

