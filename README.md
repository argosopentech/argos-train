# Argos Train

Trains an [OpenNMT](https://opennmt.net/) [PyTorch](https://pytorch.org/) model and [SentencePiece](https://github.com/google/sentencepiece) tokenizer. Designed for use with [Argos Translate](https://github.com/argosopentech/argos-translate) and [LibreTranslate](https://libretranslate.com). 

Argos Translate packages are also available for [download](https://www.argosopentech.com/argospm/index/).

## Training example
```
$ argos-train-setup

...


$ argos-train
From code (ISO 639): en
To code (ISO 639): es
From name: English
To name: Spanish
Package version: 1.0
Argos version: 1.0

...

Package saved to /home/argosopentech/en_es.argosmodel
```

## Data
Uses data from the [Opus project](http://opus.nlpl.eu/) in the Moses format.

## Environment
CUDA required, tested on [vast.ai](https://vast.ai/).

## Run training
```
argos-train

```

## Docker
Docker image available at [argosopentech/argostrain](https://hub.docker.com/repository/docker/argosopentech/argostrain).

```
docker run -it argosopentech/argostrain /bin/bash

```

## Troubleshooting
- If you're running out of GPU memory reduce `batch_size` and `valid_batch_size` in `config.yml`.

## License
Licensed under either the MIT or CC0 License (same as Argos Translate)

