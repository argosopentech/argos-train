source config.sh
./reset_packaging.sh

# Convert to CTranslate
ct2-opennmt-py-converter --model_path averaged.pt --model_spec TransformerBase --output_dir converted_model --quantization int8

# Create model package
mkdir packaged_model
cp -r converted_model packaged_model/model

# Copy in sentencepiece
cp sentencepiece.model packaged_model/

# Setup Stanza sentence boundary detection
python3 -c "import stanza; stanza.download('$stanza_lang_code', dir='stanza', processors='tokenize')"
cp -r stanza packaged_model/

# Copy in metadata.json and MODEL_README.md
cp metadata.json packaged_model/
cp MODEL_README.md packaged_model/README.md

# Zip packaged model into Argos Translate model
mv packaged_model "${sl}_${tl}"
zip -r "${sl}_${tl}.argosmodel" "${sl}_${tl}"

