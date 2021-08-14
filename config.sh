export sl="en"
export tl="zh"
export stanza_lang_code=$sl

############
# Optional #
############

export character_coverage=0.9995

# Special Tokens
# https://github.com/argosopentech/argos-translate/discussions/65
# https://github.com/google/sentencepiece/blob/master/doc/special_symbols.md
export special_tokens='<define>,<detect-sentence-boundaries>,<sentence-boundary>'

# src_vocab_size/target_vocab_size also need to be updated in config.yml
export vocab_size=50000
