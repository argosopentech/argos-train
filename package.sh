source config.sh
./reset_packaging.sh

echo "Averaging checkpoints"
./../OpenNMT-py/tools/average_models.py -m \
	openmt.model_step_10000.pt \
	openmt.model_step_11000.pt \
	-o averaged.pt
# Debug:
# cp openmt.model_step_20000.pt averaged.pt

echo "Converting to CTranslate"
ct2-opennmt-py-converter --model_path averaged.pt --model_spec TransformerBase --output_dir ctranslate_model --quantization int8

echo "Create model package"
mkdir packaged_model
cp -r ctranslate_model packaged_model/model

echo "Copy in sentencepiece"
cp sentencepiece.model packaged_model/

echo "Setup Stanza sentence boundary detection"
python3 -c "import stanza; stanza.download('$stanza_lang_code', dir='stanza', processors='tokenize')"
cp -r stanza packaged_model/

echo "Copy in metadata.json and MODEL_README.md"
cp metadata.json packaged_model/
cp MODEL_README.md packaged_model/README.md

echo "Zip packaged model into Argos Translate model"
mv packaged_model "${sl}_${tl}"
zip -r "${sl}_${tl}.argosmodel" "${sl}_${tl}"

