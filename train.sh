#!/bin/bash

# set relevant paths
vocab_size=32000
sl=en
tl=es

rm -f raw_data/all.txt
cp raw_data/source.$sl raw_data/all.txt
cat raw_data/source.$tl >> raw_data/all.txt

spm_train --input=raw_data/all.txt --model_prefix=sentencepiece \
           --vocab_size=$vocab_size --character_coverage=1

mkdir -p tokenized
spm_encode --model=sentencepiece.model < raw_data/source.$sl > tokenized/train.$sl
spm_encode --model=sentencepiece.model < raw_data/source.$tl > tokenized/train.$tl

onmt-build-vocab --from_format sentencepiece --from_vocab sentencepiece.vocab --save_vocab tokenized/vocab.vocab

export CUDA_VISIBLE_DEVICES=0
onmt-main --model_type Transformer \
          --config config.yml --auto_config \
          train --with_eval
