apt-get update && apt-get upgrade -y
pip install --upgrade pip
pip install OpenNMT-tf
python3 -m pip install ctranslate2

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

