# Argos Train

Trains an OpenNMT model and a SentencePiece parser then packages them with a Stanza model for use with [Argos Translate](https://github.com/argosopentech/argos-translate). 

Argos Translate packages are available for [download](https://www.argosopentech.com/argospm/index/).

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

## Using screen (helpful for keeping a terminal open)
Start screen:
```
screen

```
Detaching:
```
Ctrl-a d

```
Reattaching:
```
screen -r

```

[Scrolling](https://unix.stackexchange.com/questions/40242/scroll-inside-screen-or-pause-output)

## Troubleshooting
- If you're running out of GPU memory reduce `batch_size` and `valid_batch_size` in `config.yml`.

## License
Licensed under either the MIT or CC0 License (same as Argos Translate)

