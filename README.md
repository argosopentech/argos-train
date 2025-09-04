# Argos Train

Argos Train trains an [OpenNMT](https://opennmt.net/) PyTorch [Transformer](https://en.wikipedia.org/wiki/Transformer_(machine_learning_model)) model and a [SentencePiece](https://github.com/google/sentencepiece) tokenizer and packages them with [Stanza](https://stanfordnlp.github.io/stanza/) data as an Argos Translate package. Argos Translate packages, which are zip archives with a .argosmodel extension, can be used with [Argos Translate](https://github.com/argosopentech/argos-translate) and [LibreTranslate](https://libretranslate.com). 

Pre-trained Argos Translate packages are available for [download](https://www.argosopentech.com/argospm/index/). If you have trained packages you're willing to share please [get in contact](https://community.libretranslate.com/t/contributing-a-trained-language-model-package-to-argos-translate/308) so that they can be published on the [Argos Translate package index](https://github.com/argosopentech/argospm-index).

[LibreTranslate/Locomotive](https://github.com/LibreTranslate/Locomotive) has similar functionality to Argos Train and can also be used to train translation models.

## Training example

From inside argosopentech/argostrain Docker container:

```
su argosopentech
cd /home/argosopentech
export HOME="/home/argosopentech"
source ~/argos-train-init

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

To train a model with custom data add your data to `data-index.json` after running `argos-train-init` with a link to download your custom data package. Data packages are zipped directories with a .argosdata extension ([example](http://data.argosopentech.com/data-wikimedia-en_sk.argosdata)) that contain a `source` and `target` file with parallel data in corresponding lines and a `metadata.json` file. The data packages are downloaded with HTTP and you will need to run a web server like Nginx to host custom data.

You can also manually load data by putting your data at `run/source` and `run/target` and setting `data_exists=True` in `bin/argos-train`.

You can use [this project](https://github.com/Interaction-Bot/opus-nlp-downloader) to automatically download data from Opus.

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
CUDA required, tested on [vast.ai](http://vast.ai/?ref=24817).

Vast.ai seems to reckognize the CUDA version of the Docker container incorrectly so you may need to check the "Incompatible Machines" option if you're using vast.ai.

## Manually creating an Argos Translate package
If you don't want to use Argos Train you can manually train a model with [OpenNMT](https://opennmt.net/) and package it for Argos Translate. Argos Translate packages are a zip archive with a .argosmodel extension containing; a CTranslate2 model, a SentencePiece model, a Stanza 1.1.1 model, and a metadata file. Reference the training script at [bin/argos-train](bin/argos-train) for more information.

- [Example packages](https://www.argosopentech.com/argospm/index/)

## Documentation
- [Video tutorial](https://www.youtube.com/watch?v=Vj_qgnhOEwg)
- [Windows and Docker tutorial](https://community.libretranslate.com/t/training-an-argos-translation-model-locally-on-windows/588)

## Contributing
Contributions are welcome! Please make a pull request. 
##### Roadmap
- [Add finetuning support](https://github.com/argosopentech/argos-train/issues/12)


## License
Licensed under either the MIT or Creative Commons CC0 License

