# Argos Train

[Argos Translate](https://github.com/argosopentech/argos-translate) | [Video tutorial](https://odysee.com/@argosopentech:7/training-an-Argos-Translate-model-tutorial-2022:2?r=DMnK7NqdPNHRCfwhmKY9LPow3PqVUUgw)

Argos Train trains an [OpenNMT](https://opennmt.net/) PyTorch [Transformer](https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)) model and a [SentencePiece](https://github.com/google/sentencepiece) tokenizer and packages them with [Stanza](https://stanfordnlp.github.io/stanza/) data as an Argos Translate package. Argos Translate packages, which are zip archives with a .argosmodel extension, can be used with [Argos Translate](https://github.com/argosopentech/argos-translate), [LibreTranslate](https://libretranslate.com), and [Dot Lexicon](https://github.com/dothq/lexicon). 

Pre-trained Argos Translate packages are available for [download](https://www.argosopentech.com/argospm/index/). If you have trained packages you're willing to share please [get in contact](https://community.libretranslate.com) so that they can be published on the [Argos Translate package index](https://github.com/argosopentech/argospm-index).

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

To train a model with custom data add your data to `data-index.json` after running `argos-train-init` with a link to download a data package. Data packages are [zipped directory with a .argosdata extension](http://data.argosopentech.com/data-wikimedia-en_sk.argosdata) that contain a `source` and `target` file with parallel data in corresponding lines.

## Docker
Docker image available at [argosopentech/argostrain](https://hub.docker.com/repository/docker/argosopentech/argostrain).

```
docker run -it argosopentech/argostrain /bin/bash

```

## Run training
```
argos-train

```

## Environment
CUDA required, tested on [vast.ai](https://vast.ai/).

## License
Licensed under either the MIT or CC0 License (same as [Argos Translate](https://www.argosopentech.com/)).

