# pip install argostranslate
# pip install sacrebleu

SOURCE_CODE="en"
TARGET_CODE="de"

mkdir -p run

rm -f run/bleu_source run/bleu_target

sacrebleu -t wmt17 -l $SOURCE_CODE-$TARGET_CODE --echo src > run/bleu_source

while read in; do
    echo $in
    argos-translate -f $SOURCE_CODE -t $TARGET_CODE "$in" >> run/bleu_target
done < run/bleu_source

sacrebleu -i run/bleu_target -t wmt17 -l $SOURCE_CODE-$TARGET_CODE
