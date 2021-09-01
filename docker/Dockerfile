FROM nvidia/cuda:11.3.0-devel-ubuntu20.04

RUN echo "export DEBIAN_FRONTEND=noninteractive" >> /etc/profile

RUN apt-get update
RUN apt-get install -y sudo

RUN useradd -ms /bin/bash argosopentech
RUN passwd -d argosopentech
RUN usermod -aG sudo argosopentech

COPY argostrain-init.sh /home/argosopentech/
RUN chown argosopentech:argosopentech /home/argosopentech/argostrain-init.sh

