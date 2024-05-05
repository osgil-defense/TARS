from langchain_community.tools import DuckDuckGoSearchRun
from subprocess import Popen, PIPE
from urllib.parse import urlparse
from crewai_tools import tool
import validators
import socket
import subprocess
import sys
import os


def load_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def get_ip(url):
    if not validators.url(url):
        raise Exception(f"Url {url} is not a valid URL")
    root = urlparse(url).netloc
    return socket.gethostbyname(root)


RUSTSCAN_DOCS = load_file(
    os.path.join(str("/".join(__file__.split("/")[:-1])), "assets/rustscan_docs.md")
)


@tool("RustScan")
def rustscan(address: str) -> str:
    """
    Scan one address using RustScan

    Parameters:
    - addresses (str): single address or hosts to be scanned

    Returns:
    - str: The results of the RustScan or an error message.
    """

    # convert url to IP address to make things easier
    url = address
    if validators.url(url):
        url = get_ip(url)

    process = subprocess.Popen(
        f"rustscan -a {url}",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error executing RustScan: {stderr.decode('utf-8')}")

    return stdout.decode("utf-8")


@tool("RustScan")
def rustscan(
    addresses: str,
    ports: str = None,
    range_ports: str = None,
    exclude_ports: str = None,
    batch_size: int = 4500,
    timeout: int = 1500,
    tries: int = 1,
    ulimit: int = None,
    greppable: bool = False,
    no_config: bool = False,
    accessible: bool = False,
    top_ports: bool = False,
    scan_order: str = "serial",
    command: str = None,
) -> str:
    """
    Executes a RustScan scan and returns the results.

    Parameters:
    - addresses (str): Comma-separated addresses or hosts to be scanned.
    - ports (str, optional): Comma-separated list of ports to scan (e.g., "80,443").
    - range_ports (str, optional): Range of ports to scan (e.g., "1-1000").
    - exclude_ports (str, optional): Comma-separated list of ports to exclude (e.g., "21,22").
    - batch_size (int, optional): The batch size for port scanning.
    - timeout (int, optional): Timeout in milliseconds before a port is assumed to be closed.
    - tries (int, optional): Number of tries before a port is assumed to be closed.
    - ulimit (int, optional): Automatically ups the ULIMIT to the value provided.
    - greppable (bool, optional): Outputs only the ports, no Nmap.
    - no_config (bool, optional): Ignores the configuration file.
    - accessible (bool, optional): Accessible mode for better screen reader compatibility.
    - top_ports (bool, optional): Scan only the top 1000 most common ports.
    - scan_order (str, optional): Order of port scanning, 'serial' or 'random'.
    - command (str, optional): Additional command for Nmap or other further actions.

    Returns:
    - str: The results of the RustScan or an error message.
    """

    base_command = f"rustscan -a {addresses}"

    if ports:
        base_command += f" -p {ports}"
    if range_ports:
        base_command += f" -r {range_ports}"
    if exclude_ports:
        base_command += f" -e {exclude_ports}"
    if batch_size:
        base_command += f" -b {batch_size}"
    if timeout:
        base_command += f" -t {timeout}"
    if tries:
        base_command += f" --tries {tries}"
    if ulimit:
        base_command += f" -u {ulimit}"
    if greppable:
        base_command += " -g"
    if no_config:
        base_command += " -n"
    if accessible:
        base_command += " --accessible"
    if top_ports:
        base_command += " --top"
    if scan_order:
        base_command += f" --scan-order {scan_order}"
    if command:
        base_command += f" -- {command}"

    # Execute the command using subprocess
    process = subprocess.Popen(
        base_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error executing RustScan: {stderr.decode('utf-8')}")

    return stdout.decode("utf-8")


@tool("RustScanDocs")
def rustscan_docs() -> str:
    """
    Grab the entire RustScan documentation

    Returns:
    - str: Latest RustScan documentation with examples
    """

    process = subprocess.Popen(
        f"rustscan -h", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Error executing RustScan: {stderr.decode('utf-8')}")

    help_output = (
        f"# RustScan Help Output\n\n```{stdout.decode('utf-8')}```\n\n{RUSTSCAN_DOCS}"
    )

    return help_output
