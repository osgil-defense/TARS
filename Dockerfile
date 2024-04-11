FROM kalilinux/kali-rolling

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y nmap burpsuite wireshark metasploit-framework aircrack-ng \
    john sqlmap autopsy

RUN apt-get install -y vim python3-pip git

WORKDIR /root

CMD ["bash"]

