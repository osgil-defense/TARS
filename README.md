# TARS

## Vision

Create a tool to automate the process of pentesting, allowing pentesters to do more with less and in turn make the world more secure.

## How To Run

Build the image

```
docker build -t klinux .
```

Run the image as a container

```
docker run -p 8501:8501 klinux
```

Check out the app at: http://localhost:8501/

## Events

(May 5, 2024) Got the Zaproxy tool working but it needs some work. A lot of tools/finetuning.

(April 29, 2024) We are no longer participating in the Google Hackathon because Gemnei is a flawed LLM. GPT-4 seems to be the only LLM, right now, that works great for agents

(April 24, 2024) We are competing in the followign Hackathon: https://googleai.devpost.com/

## Optional Tools To Add

- [X] [Nettacker](https://github.com/OWASP/Nettacker)
- [X] [RustScan](https://github.com/RustScan/RustScan)
- [ ] [ZAP](https://www.zaproxy.org/)
- [X] [nmap](https://github.com/nmap/nmap)
- [ ] [john the ripper](https://github.com/openwall/john)
- [ ] [sqlmap](https://github.com/sqlmapproject/sqlmap)
- [ ] [aircrack-ng](https://github.com/aircrack-ng/aircrack-ng)
- [ ] [burp suite](https://portswigger.net/burp)
- [ ] [wireshark](https://www.wireshark.org/)
- [ ] [metasploit framework](https://www.metasploit.com/)

