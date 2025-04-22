FROM ubuntu

RUN apt update
RUN apt -y install bash iproute2 net-tools tcpdump vim iputils-ping
RUN apt update && apt-get install -y iptables
RUN apt clean

CMD ["bash"]
