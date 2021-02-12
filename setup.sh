apt-get update && apt-get upgrade -y
apt-get install python3 python3-pip zip -y
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

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

