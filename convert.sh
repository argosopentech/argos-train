# Averaging checkpoints
onmt-main --config config.yml --auto_config average_checkpoints --output_dir averaged_model --max_count 5

# Convert to CTranslate
ct2-opennmt-tf-converter --model_path averaged_model --model_spec TransformerBase --output_dir converted_model --src_vocab tokenized/vocab.vocab --tgt_vocab tokenized/vocab.vocab --quantization int8

# Create model package
mkdir packaged_model
cp -r converted_model packaged_model/
cp sentencepiece.model packaged_model/

