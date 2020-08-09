# onmt-models
Training script for OpenNMT models

1. Install NVIDIA drivers
2. Install Docker
3. Start Docker container 

sudo docker run --gpus all -it --name cuda -p 6006:6006 nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04 bash

4. Inside of Docker container install OpenNMT

apt-get update && apt-get upgrade -y
pip install --upgrade pip
pip install OpenNMT-tf

5. Download and install SentencePiece from source

cd
apt-get install cmake build-essential pkg-config libgoogle-perftools-dev vim git -y
git clone https://github.com/google/sentencepiece.git
cd sentencepiece
mkdir build
cd build
cmake ..
make -j $(nproc)
make install
ldconfig -v
cd

6. Download training script

git clone https://github.com/argosopentech/onmt-models.git

7. Move data directory into root of onmt-models
8. Update information about your training data in the top of onmt-models/train.sh
9. From the top level of the onmt-models directory run train.sh
