source config.sh

mkdir checkpoint_export
cp -r averaged_model checkpoint_export/
cp sentencepiece.model checkpoint_export/
cp sentencepiece.vocab checkpoint_export/
mv checkpoint_export "checkpoint_export_${sl}_${tl}"
zip -r "checkpoint_export_${sl}_${tl}.zip" "checkpoint_export_${sl}_${tl}"

