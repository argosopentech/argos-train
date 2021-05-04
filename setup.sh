# Install Debian packages
sudo apt-get update && apt-get upgrade -y
sudo apt-get install python3 python3-pip zip -y

# Install Python
python3 -m pip install --upgrade pip
cd ~/onmt-models
python3 -m pip install .

# Compile SentencePiece
cd
sudo apt-get install cmake build-essential pkg-config libgoogle-perftools-dev vim git -y
git clone https://github.com/google/sentencepiece.git
cd sentencepiece
mkdir build
cd build
cmake ..
make -j $(nproc)
sudo make install
sudo ldconfig -v

# Install OpenNMT-py
cd
git clone https://github.com/OpenNMT/OpenNMT-py.git
cd OpenNMT-py
pip3 install -e .
pip3 install -r requirements.opt.txt


