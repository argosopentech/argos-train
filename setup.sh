# Based on OpenNMT example scripts
# https://github.com/OpenNMT/OpenNMT-tf/tree/master/scripts/wmt

# Config
sl="en"
tl="es"
data_dir="data"
src_data="$data_dir/en-es.en"
tgt_data="$data_dir/en-es.es"
vocab_size=32000

do_install_sentencepiece=1

# Install SentencePiece from source
if [ $do_install_sentencepiece -gt 0 ]
then
	echo "Installing SentencePiece"
	git clone https://github.com/google/sentencepiece.git
	sudo apt-get install -y cmake build-essential pkg-config libgoogle-perftools-dev
	cd sentencepiece
	mkdir build
	cd build
	cmake ..
	make -j $(nproc)
	sudo make install
	sudo ldconfig -v
	cd ../..
fi

# Train SentencePiece
echo "Training SentencePiece"
cat $src_data > $data_dir/all.txt
cat $tgt_data >> $data_dir/all.txt
spm_train --input=all.txt --model_prefix=wmtenes --input_sentence_size=10000000 --shuffle_input_sentence=true --vocab_size=$vocab_size --character_coverage=1
rm $data_dir/all.txt

# Use SentencePiece
echo "Running SentencePiece"
spm_encode --model=wmt$sl$tl.model < $src_data > $data_dir/train.$sl
spm_encode --model=wmt$sl$tl.model < $tgt_data > $data_dir/train.$tl

# Prepare vocab for OpenNMT-tf
echo "Setting up vocab"
onmt-build-vocab --from_format sentencepiece --from_vocab wmt$sl$tl.vocab --save_vocab $data_dir/wmt$sl$tl.vocab
