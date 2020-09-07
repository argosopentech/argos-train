source config.sh

virtualenv env
source env/bin/activate
python3 -m pip install stanza
python3 -c "import stanza; stanza.download('$stanza_lang_code', dir='stanza', processors='tokenize')"
