FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y sudo

RUN useradd -ms /bin/bash argosopentech
RUN passwd -d argosopentech
RUN echo "argosopentech ALL=(ALL:ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/argosopentech
RUN usermod -aG sudo argosopentech

COPY bin/argos-train-init /home/argosopentech/
RUN chown argosopentech:argosopentech /home/argosopentech/argos-train-init
RUN chmod 774 /home/argosopentech/argos-train-init

