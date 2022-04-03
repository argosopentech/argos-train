# Argos Train

[Argos Translate](https://github.com/argosopentech/argos-translate) | [Video tutorial](https://odysee.com/@argosopentech:7/training-an-Argos-Translate-model-tutorial-2022:2?r=DMnK7NqdPNHRCfwhmKY9LPow3PqVUUgw)

Trains an [OpenNMT](https://opennmt.net/) PyTorch model and [SentencePiece](https://github.com/google/sentencepiece) tokenizer and packages them for use with [Argos Translate](https://github.com/argosopentech/argos-translate) and [LibreTranslate](https://libretranslate.com). 

Pre-trained Argos Translate packages are available for [download](https://www.argosopentech.com/argospm/index/). If you have trained models you're willing to share please reach out so they can be published on the [package index](https://github.com/argosopentech/argospm-index).

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
Version: 1.0

...

Package saved to /home/argosopentech/argos-train/run/en_es.argosmodel
```

## Data
Data from [data-index.json](/data-index.json) is used for training. Argos Translate primarily uses data from the [Opus project](http://opus.nlpl.eu/). 

To train a model with custom data add your data to `data-index.json` after running `argos-train-init` with a link to download a data package. Data packages are [zip archives with a .argosdata extension](http://data.argosopentech.com/data-wikimedia-en_sk.argosdata).

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

