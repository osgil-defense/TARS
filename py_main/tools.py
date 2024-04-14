from langchain_community.tools import DuckDuckGoSearchRun
import subprocess
from subprocess import Popen, PIPE
from crewai_tools import tool
import requests
import json
import os


@tool("NotifyCyberGetPastWeekData")
def get_past_week_data():
    """
    Get the latest cybersecurity news in the last 7 days from Notify Cyber

    Raises:
        ValueError: If the NC_API_TOKEN environment variable is not set.
        Exception: If the API request fails.

    Returns:
        JSON response from the API.
    """
    auth_token = os.getenv("NC_API_TOKEN")
    if not auth_token:
        raise ValueError("NC_API_TOKEN environment variable is not set")

    url = "https://nc-api.vercel.app/past_week"
    response = requests.get(url, headers={"Authorization": auth_token})

    if response.ok:
        output = response.json()

        # (April 13, 2024) this is a very janky fix for the token limit issue with a model
        output = output[:10]

        return output
    else:
        raise Exception(
            f"Failed to fetch past week data: {response.status_code} - {response.text}"
        )


@tool("NotifyCyberSearch")
def search_data(queries: list):
    """
    Search for key words in a cybersecurity news database hosted by Notify Cyber

    Parameters:
        queries (list of str): List of keywords to search for from the API.

    Raises:
        ValueError: If the NC_API_TOKEN environment variable is not set, if queries is not a list of strings, or if any query is not a string.
        Exception: If the API request fails.

    Returns:
        JSON response from the API.
    """
    if not isinstance(queries, list) or not all(
        isinstance(query, str) for query in queries
    ):
        raise ValueError("Queries must be a list of strings")

    auth_token = os.getenv("NC_API_TOKEN")
    if not auth_token:
        raise ValueError("NC_API_TOKEN environment variable is not set")

    # Joining the list of queries into a single string separated by commas
    query_string = ",".join(queries)
    url = f"https://nc-api.vercel.app/search?{query_string}"
    response = requests.get(url, headers={"Authorization": auth_token})
    if response.ok:
        output = response.json()
        
        # (April 13, 2024) this is a very janky fix for the token limit issue with a model
        output = output[:10]
        
        return output
    else:
        raise Exception(f"Failed to search: {response.status_code} - {response.text}")


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

    # print(f"Running Nmap: {command}")

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
