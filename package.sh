source config.sh

# Remove old package runs
rm -rf run/averaged.pt run/stanza run/ctranslate_model run/packaged_model "run/${sl}_${tl}" run/*.argosmodel

echo "Averaging checkpoints"
./../OpenNMT-py/tools/average_models.py -m \
	run/openmt.model_step_49000.pt \
	run/openmt.model_step_50000.pt \
	-o run/averaged.pt
# Debug:
#cp openmt.model_step_50000.pt averaged.pt

echo "Converting to CTranslate"
ct2-opennmt-py-converter --model_path run/averaged.pt --output_dir run/ctranslate_model --quantization int8

echo "Create model package"
mkdir run/packaged_model
cp -r run/ctranslate_model run/packaged_model/model

echo "Copy in sentencepiece"
cp run/sentencepiece.model run/packaged_model/

echo "Setup Stanza sentence boundary detection"
python3 -c "import stanza; stanza.download('$stanza_lang_code', dir='run/stanza', processors='tokenize')"
cp -r run/stanza run/packaged_model/

echo "Copy in metadata.json and MODEL_README.md"
cp metadata.json run/packaged_model/
cp MODEL_README.md run/packaged_model/README.md

echo "Zip packaged model into Argos Translate model"
mv run/packaged_model "run/${sl}_${tl}"
zip -r "run/${sl}_${tl}.argosmodel" "run/${sl}_${tl}"

