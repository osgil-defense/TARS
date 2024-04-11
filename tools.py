from langchain_community.tools import DuckDuckGoSearchRun
import subprocess
from subprocess import Popen, PIPE
from crewai_tools import tool
import requests


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

    # Execute the nmap command
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return f"Error executing nmap: {stderr.decode('utf-8')}"

    return stdout.decode("utf-8")


@tool("CurlTool")
def curl_tool(
    url: str, method: str = "GET", headers: dict = None, data: dict = None
) -> str:
    """Executes curl commands and returns the response."""
    curl_cmd = ["curl", "-X", method, url]

    if headers:
        for key, value in headers.items():
            curl_cmd.extend(["-H", f"{key}: {value}"])

    if data:
        curl_cmd.extend(["-d", str(data)])

    process = subprocess.Popen(curl_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        return stdout.decode("utf-8")
    return stderr.decode("utf-8")


@tool("GetLocalIp")
def get_external_ip(ip=None):
    """Get external ip address or provide one"""
    try:
        if ip != None:
            return str(ip)
        response = requests.get("https://api.ipify.org")
        return str(response.text)
    except:
        return None


@tool("DuckDuckGoSearch")
def search(query: str):
    """Search the web for information on a given topic"""
    return DuckDuckGoSearchRun().run(query)


@tool("ExecuteUnixCmd")
def execute_unix_cmd(command: str) -> str:
    """Execute Unix commands in a unix-based shell"""
    if command is None:
        raise ValueError("Command is required")

    process = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        return f"Error executing command: {stderr.decode('utf-8')}"

    return stdout.decode("utf-8")
