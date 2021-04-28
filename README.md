# Argos Translate training script

Trains an OpenNMT model and a SentencePiece parser then packages them with a Stanza model for use with [Argos Translate](https://github.com/argosopentech/argos-translate). 

Argos Translate packages available for download [here](https://drive.google.com/drive/folders/11wxM3Ze7NCgOk_tdtRjwet10DmtvFu3i).

## Data
Uses data from the [Opus project](http://opus.nlpl.eu/) in the Moses format.

## Environment
This is the setup currently used to train models:
- NVIDIA Tesla K80 GPU
- 7 cores, 30GB Memory
- 75-200GB swap space
- Ubuntu 20.04

## Install CUDA
Tested on Ubuntu 20.04 with [this script](https://github.com/PJ-Finlay/cuda-setup):


**Warning: This uninstalls XOrg and should only be run on a headless server**


```
curl https://raw.githubusercontent.com/PJ-Finlay/cuda-setup/main/setup_cuda.sh | sh
sudo reboot

```
Using the nvidia/cuda Docker container should also work.

## Install training dependencies
```
cd
git clone https://github.com/argosopentech/onmt-models.git
cd ~/onmt-models
sudo ./setup.sh

```

## Download data
```
cd ~/onmt-models/raw_data
wget https://object.pouta.csc.fi/OPUS-Wikipedia/v1.0/moses/en-es.txt.zip
unzip en-es.txt.zip
cat *.en >> source
cat *.es >> target

```

## Add swap space
75GB works for most models, if you have free disk space you can do more.
```
sudo fallocate -l 75G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo swapon --show

```

## Start screen (optional)
```
screen

```

## Run training
```
argos-train

```

## Using screen (if you started it)
Detaching:
```
Ctrl-a d

```
Reattaching:
```
screen -r

```
[Scrolling](https://unix.stackexchange.com/questions/40242/scroll-inside-screen-or-pause-output)

## Packaging
### Edit metadata (optional)
`metadata.json` example:
```
{
    "package_version": "1.0",
    "argos_version": "1.1",
    "from_code": "en",
    "from_name": "English",
    "to_code": "zh",
    "to_name": "Chinese"
}
```

`MODEL_README.md` is a Markdown document that will be packaged with your model.

## Package for Argos Translate
```
./package.sh
```

## Useful scripts
- `./reset.sh` - Reset training but leave data.

## Troubleshooting
- If you're running out of GPU memory reduce `batch_size` and `valid_batch_size` in `config.yml`.

## Making an Argospm package
- Download data from Opus
    - Use as many as you can. For many languages there's a big dropoff in size after the first few datasets so I generally only bother with the large ones.
    - Cite each dataset in `MODEL_README.md`
    - Only use freely licensed datasets. Some of the datasets have non commercial restrictions.
 - Download Wikimedia data
    -  Download pre extraced dictionaries from: [https://github.com/tatuylonen/wiktextract](https://github.com/tatuylonen/wiktextract)   
    -  [https://kaikki.org/dictionary/](https://kaikki.org/dictionary/)
    -  `source config.sh && generate-wiktionary-data kaikki.org-dictionary-Irish.json kaikki.org-dictionary-English.json`
 - Combine datasets
     - `cd raw_data && cat *.zh >> source && cat *.en >> target`


## License
Licensed under either the MIT or CC0 License (same as Argos Translate)

