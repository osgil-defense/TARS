from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import ShellTool
from subprocess import Popen, PIPE
from crewai_tools import tool
import subprocess
import requests
import platform
import os


def ping(hostname):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", hostname]
    response = subprocess.run(
        command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    return response.returncode == 0


@tool("ScanSubdomains")
def scan_subdomains(website: str):
    """Run a Nettacker command to scan subdomains of the given website"""

    if website is None:
        raise ValueError("Website is required")

    if ping(website) == False:
        raise Exception("Website does not exist you fat donkey")

    cmd = f"nettacker -i {website} -s -m port_scan -t 10 -M 35 -g 20-100"
    if os.getenv("DEVELOPER_MODE") == True:
        cmd = f"python3 nettacker.py -i {website} -s -m port_scan -t 10 -M 35 -g 20-100"

    shell_tool = ShellTool()
    subdomains = shell_tool.run({"commands": [cmd]})

    print(str(subdomains))
    return str(subdomains)


@tool("GetLocalIp")
def get_external_ip():
    """Get external ip address or provide one"""
    try:
        response = requests.get("https://api.ipify.org", timeout=15)
        return str(response.text)
    except:
        return None


@tool("DuckDuckGoSearch")
def search(query: str):
    """Search the web for information on a given topic"""
    return DuckDuckGoSearchRun().run(query)


@tool("NmapTool")
def nmap_tool(target: str, options: str = "") -> str:
    """
    Executes nmap commands and returns the network scan results.

    Parameters:
    - target (str): The IP address, hostname, or network to scan.
    - options (str): Additional command-line options for nmap.
    """

    if not target:
        raise ValueError("Target is required for nmap scanning.")

    command = f"nmap {options} {target}"

    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return f"Error executing nmap: {stderr.decode('utf-8')}"

    return stdout.decode("utf-8")
