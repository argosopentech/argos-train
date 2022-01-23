# Argos Train

[Argos Translate](https://github.com/argosopentech/argos-translate) | [Video tutorial](https://odysee.com/@argosopentech:7/training-an-Argos-Translate-model-tutorial-2022:2?r=DMnK7NqdPNHRCfwhmKY9LPow3PqVUUgw)

Trains an [OpenNMT](https://opennmt.net/) PyTorch model and [SentencePiece](https://github.com/google/sentencepiece) tokenizer. Designed for use with [Argos Translate](https://github.com/argosopentech/argos-translate) and [LibreTranslate](https://libretranslate.com). 

Pre-trianed Argos Translate packages are also available for [download](https://www.argosopentech.com/argospm/index/).

## Training example
```
$ su argosopentech
$ source ~/argos-train-init

...


$ argos-train
From code (ISO 639): en
To code (ISO 639): es
From name: English
To name: Spanish
Package version: 1.0
Argos version: 1.0

...

Package saved to /home/argosopentech/argos-train/run/en_es.argosmodel
```

## Data
Uses data from the [Opus project](http://opus.nlpl.eu/) in the Moses format stored in [data index](/data-index.json).

## Environment
CUDA required, tested on [vast.ai](https://vast.ai/).

## Docker
Docker image available at [argosopentech/argostrain](https://hub.docker.com/repository/docker/argosopentech/argostrain).

```
docker run -it argosopentech/argostrain /bin/bash

```

## Run training
```
argos-train

```

## Troubleshooting
- If you're running out of GPU memory reduce `batch_size` and `valid_batch_size` in `config.yml`.

## License
Licensed under either the MIT or CC0 License (same as [Argos Translate](https://www.argosopentech.com/)).

