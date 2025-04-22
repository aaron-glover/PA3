FROM ubuntu:latest

RUN apt-get update && \
        apt-get install -y curl gnupg lsb-release net-tools iproute2 iputils-ping && \
        curl -s https://deb.frrouting.org/frr/keys.gpg | tee /usr/share/keyrings/frrouting.gpg > /dev/null && \
        echo deb '[signed-by=/usr/share/keyrings/frrouting.gpg]' https://deb.frrouting.org/frr \
        $(lsb_release -s -c) frr-stable | tee -a /etc/apt/sources.list.d/frr.list && \
        apt-get update && \
        apt-get install -y frr frr-pythontools

# Ensure ospfd is enabled by default
RUN sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons

CMD ["sleep", "infinity"]
