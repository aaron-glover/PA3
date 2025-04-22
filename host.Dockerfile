FROM ubuntu

RUN apt-get update
RUN apt-get -y install bash iproute2 net-tools tcpdump vim iputils-ping
RUN apt-get update && apt-get install -y iptables
RUN apt-get clean

CMD ["bash"]
