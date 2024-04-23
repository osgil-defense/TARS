FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# install dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y nmap sqlmap autopsy john
RUN apt-get install -y vim python3-pip git python-is-python3

# segmented run layers so that compiler does not shit pants
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# install, manually, nettacker
RUN mkdir /opt/nettacker
RUN git clone https://github.com/OWASP/Nettacker.git /opt/nettacker
RUN pip3 install -r /opt/nettacker/requirements.txt
RUN chmod +x /opt/nettacker/nettacker.py
RUN ln -s /opt/nettacker/nettacker.py /usr/local/bin/nettacker

# install project's depends
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

WORKDIR /root

CMD ["bash"]

