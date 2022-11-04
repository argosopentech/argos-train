FROM nvidia/cuda:11.8.0-devel-ubuntu22.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y sudo

RUN useradd -ms /bin/bash argosopentech
RUN passwd -d argosopentech
RUN usermod -aG sudo argosopentech

COPY bin/argos-train-init /home/argosopentech/
RUN chown argosopentech:argosopentech /home/argosopentech/argos-train-init
RUN chmod 774 /home/argosopentech/argos-train-init

# Disable tmux for vast.ai
RUN touch /root/.no_auto_tmux

