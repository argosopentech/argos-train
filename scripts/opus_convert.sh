# Example Output:

# pj@pj-Latitude-5490:~/git/argos-train$ ./scripts/opus_convert.sh
# From code:
# en
# To code:
# is
# URL:
# https://object.pouta.csc.fi/OPUS-ParaCrawl/v9/moses/en-is.txt.zip
# Slug:
# data-paracrawl-en_is
# --2025-06-05 18:21:58--  https://object.pouta.csc.fi/OPUS-ParaCrawl/v9/moses/en-is.txt.zip
# Resolving object.pouta.csc.fi (object.pouta.csc.fi)... 86.50.254.18, 86.50.254.19
# Connecting to object.pouta.csc.fi (object.pouta.csc.fi)|86.50.254.18|:443... connected.
# HTTP request sent, awaiting response... 200 OK
# Length: 234578721 (224M) [application/zip]
# Saving to: ‘en-is.txt.zip’
#
# en-is.txt.zip       100%[===================>] 223.71M   898KB/s    in 3m 35s
#
# 2025-06-05 18:25:34 (1.04 MB/s) - ‘en-is.txt.zip’ saved [234578721/234578721]
#
# Archive:  en-is.txt.zip
#   inflating: README
#   inflating: LICENSE
#   inflating: ParaCrawl.en-is.en
#   inflating: ParaCrawl.en-is.is
#   inflating: ParaCrawl.en-is.xml
# Opus slug:
# ParaCrawl.en-is
# 2967579 data-paracrawl-en_is/source
# Enter to continue
#
#   adding: data-paracrawl-en_is/ (stored 0%)
#   adding: data-paracrawl-en_is/metadata.json (deflated 41%)
#   adding: data-paracrawl-en_is/source (deflated 60%)
#   adding: data-paracrawl-en_is/target (deflated 62%)
#   adding: data-paracrawl-en_is/LICENSE (deflated 60%)
#   adding: data-paracrawl-en_is/README (deflated 48%)





echo "From code:"
read from
echo "To code:"
read to
echo "URL:"
read url
echo "Slug (ex: data-nllb-en_de):"
read slug
wget $url
unzip *.txt.zip
rm *.txt.zip
mkdir $slug
mv README LICENSE $slug

#cp ../metadata.json $slug
echo "{"                              >  "$slug/metadata.json"
echo "    \"name\": \"DatasetName\"," >> "$slug/metadata.json"
echo "    \"type\": \"data\","        >> "$slug/metadata.json"
echo "    \"from_code\": \"$from\","  >> "$slug/metadata.json"
echo "    \"to_code\": \"$to\","      >> "$slug/metadata.json"
echo "    \"size\": 0,"               >> "$slug/metadata.json"
echo "    \"reference\": \"Ref\""     >> "$slug/metadata.json"
echo "}"                              >> "$slug/metadata.json"


echo "Opus slug (ex: CCAligned.de-en) copy from above:"
read opus_slug
mv $opus_slug.$from $slug/source
mv $opus_slug.$to $slug/target
rm $opus_slug.*
echo "Counting number of lines"
wc -l $slug/source
echo "Copy ^ this number to paste into metadata.json in the next step"

echo "Enter to continue"
read
vim $slug/metadata.json

echo "Zipping .argosdata package"
zip -r $slug.argosdata $slug

# Uploading to data.argosopentech.com
# Run from root dir:
# scp *.argosdata root@data.argosopentech.com:/var/www/html/

