<h1 align="center">Threat Assessment & Response System (TARS)</h1>

<p align="center">
    <img width="500" src="./frontend/logo.png">
</p>

## About

TARS is our attempt towards trying to automate parts of cybersecurity penetration testing using AI agents

## Demos

| [![Video 1 Title](assets/thumbnail_1.png)](https://www.youtube.com/watch?v=HNlvgvFs43g) | [![Video 2 Title](assets/thumbnail_2.png)](https://www.youtube.com/watch?v=Sjw_gkSz6Lw) | [![Video 3 Title](assets/thumbnail_3.png)](https://www.youtube.com/watch?v=JSBVHl7PWek) |
| :-------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------: |
|                                         Demo #1                                         |                                     Demo #2 (Short)                                     |                                     Demo #3 (Long)                                      |

## Long-Term Vision

Provide intelligent defense solutions by building AI-Agent based tools for automating cybersecurity penetration testing. In short, the plan is:

1. Build agents that can properly use existing cybersecurity tools for vulnerability scanning and threat analysis.
2. Optimize those agents to automate vulnerability identification and patching, instead of just scanning and threat reporting.
3. Build a reactive defensive system that can produce countermeasures against attackers in real-time.
4. (Long Term) Develop tools to prepare for a future where advanced, dynamic, and automated AI-driven attacks can be easily deployed.

## How To Run

⚠️ Warning: TARS has been tested on macOS and some Linux distros!

1. Install [Docker](https://www.docker.com/)
2. Create a ".env" file. This file will contain all the API keys needed to make TARS function. Refer to the ".template_env" file see what you need to provide in the ".env" file for.

3. Execute TARS's main CLI tool to setup and run TARS in the browser:

```bash
bash cli.sh -r
```

4. After all of this, start using TARS with the URL provided. It most likely will be this URL: http://localhost:8501/

## Run Formatter

Keeping the code clean, consistent, and well structured requires formatting. To do formatting for this project, run the following command:

```bash
bash cli.sh -f
```

## Other Notes

### Good Test Targets

1. [Juice-Shop](https://github.com/juice-shop/juice-shop)

### Tools To Add

- [x] [Nettacker](https://github.com/OWASP/Nettacker)
- [x] [RustScan](https://github.com/RustScan/RustScan)
- [x] [ZAP](https://www.zaproxy.org/)
- [x] [nmap](https://github.com/nmap/nmap)
- [ ] [john the ripper](https://github.com/openwall/john)
- [ ] [sqlmap](https://github.com/sqlmapproject/sqlmap)
- [ ] [aircrack-ng](https://github.com/aircrack-ng/aircrack-ng)
- [ ] [burp suite](https://portswigger.net/burp)
- [ ] [wireshark](https://www.wireshark.org/)
- [ ] [metasploit framework](https://www.metasploit.com/)
