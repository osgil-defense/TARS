FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# install dependencies
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget
RUN apt-get install -y nmap sqlmap autopsy john
RUN apt-get install -y vim python3-pip git python-is-python3

# install Google Chrome
WORKDIR /home/
RUN apt-get update && apt-get install -y wget gnupg2 software-properties-common
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable
WORKDIR /root/

# install RustScan
RUN wget https://github.com/RustScan/RustScan/releases/download/2.2.2/rustscan_2.2.2_amd64.deb
RUN dpkg -i rustscan_2.2.2_amd64.deb
RUN rm rustscan_2.2.2_amd64.deb
RUN apt-get install -y iputils-ping

# segmented run layers so that compiler does not shit pants
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# install, manually, nettacker
RUN mkdir /opt/nettacker
RUN git clone https://github.com/OWASP/Nettacker.git /opt/nettacker
RUN pip3 install -r /opt/nettacker/requirements.txt
RUN chmod +x /opt/nettacker/nettacker.py
RUN ln -s /opt/nettacker/nettacker.py /usr/local/bin/nettacker

# install project's depends
COPY . /root/
RUN pip3 install -r /root/requirements.txt

WORKDIR /root/

CMD ["bash"]

