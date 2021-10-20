FROM nvidia/cuda:11.2.2-devel-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

# Disable tmux for vast.ai
RUN touch /root/.no_auto_tmux

RUN apt-get update
RUN apt-get install -y sudo

RUN useradd -ms /bin/bash argosopentech
RUN passwd -d argosopentech
RUN usermod -aG sudo argosopentech

COPY argostrain-init.sh /home/argosopentech/
RUN chown argosopentech:argosopentech /home/argosopentech/argostrain-init.sh
RUN chmod 774 /home/argosopentech/argostrain-init.sh

USER argosopentech
RUN /home/argosopentech/argostrain-init.sh
