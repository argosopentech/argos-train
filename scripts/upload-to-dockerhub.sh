#!/bin/bash
docker login -u NAME
sudo docker build -t argostrain .
sudo docker image tag argostrain argosopentech/argostrain:latest
sudo docker image push argosopentech/argostrain:latest
