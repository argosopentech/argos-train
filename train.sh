# Based on OpenNMT example scripts
# https://github.com/OpenNMT/OpenNMT-tf/tree/master/scripts/wmt

# Config
sl="en"
tl="es"
data_dir="data"
src_data="$data_dir/en-es.en"
tgt_data="$data_dir/en-es.es"
vocab_size=32000
character_coverage=1 # 0.9995 for languages with a large number of characters (Chinese) 1 for languages with a small number (English)

# Train SentencePiece
echo "Training SentencePiece (This may take a while)"
cat $src_data > $data_dir/all.txt
cat $tgt_data >> $data_dir/all.txt
spm_train --input=all.txt --model_prefix=sentencepiece --input_sentence_size=10000000 --shuffle_input_sentence=true --vocab_size=$vocab_size --character_coverage=$character_coverage
rm $data_dir/all.txt

# Use SentencePiece
echo "Running SentencePiece"
spm_encode --model=sentencepiece$sl$tl.model < $src_data > $data_dir/train.$sl
spm_encode --model=sentencepiece$sl$tl.model < $tgt_data > $data_dir/train.$tl

# Prepare vocab for OpenNMT-tf
echo "Setting up vocab"
onmt-build-vocab --from_format sentencepiece --from_vocab sentencepiece$sl$tl.vocab --save_vocab $data_dir/$sl$tl.vocab

# Train Model! (If you need to pause during this step you can do so with Ctrl-C and then resume by re-running this command)
onmt-main --model_type Transformer \
          --config config.yml --auto_config \
          train --with_eval

