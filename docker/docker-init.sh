# Install Debian packages
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip python3-virtualenv zip git -y

# Setup env
echo "export DEBIAN_FRONTEND=noninteractive" >> ~/.profile
echo 'export PATH=$PATH:~/.local/bin:~/env/bin' >> ~/.profile
source ~/.profile

# Setup Python environment
virtualenv ~/env
source env/bin/activate
git clone https://github.com/argosopentech/onmt-models.git ~/onmt-models
~/env/bin/pip install -e ~/onmt-models

# Install OpenNMT-py
git clone https://github.com/OpenNMT/OpenNMT-py.git ~/OpenNMT-py
~/env/bin/pip install -e ~/OpenNMT-py
~/env/bin/pip install -r ~/OpenNMT-py/requirements.opt.txt

# Compile SentencePiece
cd
sudo apt-get install cmake build-essential pkg-config libgoogle-perftools-dev vim git -y
git clone https://github.com/google/sentencepiece.git ~/sentencepiece
cd sentencepiece
mkdir build
cd build
cmake ..
make -j $(nproc)
sudo make install
sudo ldconfig -v


