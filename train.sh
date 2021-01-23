#!/bin/bash

# Based on OpenNMT baseline training script:
# https://github.com/OpenNMT/OpenNMT-tf/tree/master/scripts/wmt

source config.sh

echo "Splitting train and valid data"
mkdir split_data
./split_train_and_valid.py raw_data/source.$sl src
./split_train_and_valid.py raw_data/source.$tl tgt

cat split_data/*train.txt >> split_data/all.txt

spm_train --input=split_data/all.txt --model_prefix=sentencepiece \
           --vocab_size=$vocab_size --character_coverage=$character_coverage\
	   --input_sentence_size=1000000 --shuffle_input_sentence=true

onmt_build_vocab -config config.yml -n_sample -1

rm split_data/all.txt

echo "Done with tokenization"

./resume_train.sh
