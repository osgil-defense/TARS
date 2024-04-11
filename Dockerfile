FROM kalilinux/kali-rolling

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y nmap burpsuite wireshark metasploit-framework aircrack-ng \
    john sqlmap autopsy

RUN apt-get install -y vim python3-pip git

COPY requirements.txt /root/requirements.txt

RUN pip3 install -r /root/requirements.txt

WORKDIR /root

CMD ["bash"]

