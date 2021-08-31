FROM nvidia/cuda:11.4.1-cudnn8-runtime-ubuntu20.04

RUN echo "export DEBIAN_FRONTEND=noninteractive" >> /etc/profile

RUN apt-get update
RUN apt-get install -y sudo

RUN useradd -ms /bin/bash argosopentech
RUN passwd -d argosopentech
RUN usermod -aG sudo argosopentech
USER argosopentech
WORKDIR /home/argosopentech

COPY docker-init.sh /home/argosopentech/

ENTRYPOINT ["tail", "-f", "/dev/null"]

