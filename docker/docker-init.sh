
# Install Debian packages
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install python3 python3-pip python3-virtualenv zip -y

# Install Python
cd ~/onmt-models
python3 -m pip install -e .

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



