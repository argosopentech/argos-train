echo "From code:"
read from
echo "To code:"
read to
echo "URL:"
read url
echo "Slug:"
read slug
wget $url
unzip *.txt.zip
rm *.txt.zip
mkdir $slug
mv README LICENSE $slug
cp ../metadata.json $slug


echo "Opus slug:"
read opus_slug
mv $opus_slug.$from $slug/source
mv $opus_slug.$to $slug/target
rm $opus_slug.*
wc -l $slug/source

echo "Enter to continue"
read
vim $slug/metadata.json
zip -r $slug.argosdata $slug



