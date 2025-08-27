FROM ubuntu

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y sudo

RUN useradd -ms /bin/bash argosopentech && \
    passwd -d argosopentech && \
    echo "argosopentech ALL=(ALL:ALL) NOPASSWD: ALL" > /etc/sudoers.d/argosopentech && \
    usermod -aG sudo argosopentech

COPY bin/argos-train-init /home/argosopentech/
RUN chown argosopentech:argosopentech /home/argosopentech/argos-train-init && \
    chmod 774 /home/argosopentech/argos-train-init

USER argosopentech
WORKDIR /home/argosopentech
