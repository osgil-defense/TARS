FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y nmap sqlmap autopsy

RUN apt-get install -y burpsuite aircrack-ng john

RUN apt-get install -y wireshark metasploit-framework

RUN apt-get install -y vim python3-pip git python-is-python3
# Segmented run layers so that compiler does not shit pants
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /root/requirements.txt
COPY py_main /root/py_main/

RUN pip3 install -r /root/requirements.txt

WORKDIR /root

CMD ["bash"]

