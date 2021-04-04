source config.sh

echo "Splitting train and valid data"
./split_train_and_valid.py raw_data/source.$sl raw_data/source.$tl

cat split_data/*train.txt >> split_data/all.txt

spm_train --input=split_data/all.txt --model_prefix=sentencepiece \
           --vocab_size=$vocab_size --character_coverage=$character_coverage \
	   --input_sentence_size=1000000 --shuffle_input_sentence=true \
	   --user_defined_symbols=$special_tokens

onmt_build_vocab -config config.yml -n_sample -1

rm split_data/all.txt

echo "Done with tokenization"

onmt_train -config config.yml

