source config.sh
./reset_packaging.sh

# Averaging checkpoints
onmt-main --config config.yml --auto_config average_checkpoints --output_dir averaged_model --max_count 5

# Convert to CTranslate
ct2-opennmt-tf-converter --model_path averaged_model --model_spec TransformerBase --output_dir converted_model --src_vocab tokenized/vocab.vocab --tgt_vocab tokenized/vocab.vocab --quantization int8

# Create model package
mkdir packaged_model
cp -r converted_model packaged_model/model

# Copy in sentencepiece
cp sentencepiece.model packaged_model/

# Setup Stanza sentence boundary detection
./download_stanza_model.sh
cp -r stanza packaged_model/

# Copy in metadata.json and MODEL_README.md
cp metadata.json packaged_model/
cp MODEL_README.md packaged_model/README.md

# Zip packaged model into Argos Translate model
mv packaged_model "${sl}_${tl}"
zip -r "${sl}_${tl}.argosmodel" "${sl}_${tl}"

