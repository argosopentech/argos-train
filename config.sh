export sl="en"
export tl="zh"
export stanza_lang_code=$sl
export vocab_size=32000

# 1 for languages with a small character set
# 0.9995 for languages like Japanese or Chinese
export character_coverage=0.9995

# Special Tokens
# https://github.com/argosopentech/argos-translate/discussions/65
# https://github.com/google/sentencepiece/blob/master/doc/special_symbols.md
export special_tokens='<define>,<detect-sentence-boundaries>,<sentence-boundary>'

