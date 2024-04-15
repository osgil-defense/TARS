from langchain_community.tools import DuckDuckGoSearchRun
import subprocess
from subprocess import Popen, PIPE
from crewai_tools import tool
import datetime
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
def search_data(queries: list, n: int = 10):
    """
    Search for key words in a cybersecurity news database hosted by Notify Cyber.

    Parameters:
        queries (list of str): List of keywords to search for from the API.
        n (int): Number of search results to return.

    Raises:
        ValueError: If queries is not a list of strings, or if any query is not a string.
        ValueError: If n is not an integer or is less than 1.
        Exception: If the API request fails.

    Returns:
        JSON response from the API.
    """
    if not isinstance(queries, list) or not all(isinstance(query, str) for query in queries):
        raise ValueError("Queries must be a list of strings")
    if not isinstance(n, int) or n < 1:
        raise ValueError("n must be an integer greater than 0")

    auth_token = os.getenv("NC_API_TOKEN")
    if not auth_token:
        raise ValueError("NC_API_TOKEN environment variable is not set")

    # extract all NC data for each respected keyword
    all_results = {}
    for query in queries:
        response = requests.get(
            f"https://nc-api.vercel.app/search?{query}",
            headers={"Authorization": auth_token},
        )
        if response.ok:
            all_results[query] = response.json()

    # sort by source for each keyword data output
    sourced_all_results = {}
    for key in all_results:
        if key not in sourced_all_results:
            sourced_all_results[key] = {}
        for entry in all_results[key]:
            source = entry["source"]
            if source not in sourced_all_results[key]:
                sourced_all_results[key][source] = []
            sourced_all_results[key][source].append(entry)

    # distribute entry selection across sources to fill output without exceeding limit per source or total
    output = []
    existing_ids = []
    total_entries = sum(len(entries) for keyword in sourced_all_results for source, entries in sourced_all_results[keyword].items())
    entry_limit = max(1, n // max(1, total_entries))
    for keyword in sourced_all_results:
        for source in sourced_all_results[keyword]:
            count = 0
            for entry in sourced_all_results[keyword][source]:
                if len(output) < n and count < entry_limit:
                    new_id = entry["id"]
                    if new_id not in existing_ids:
                        existing_ids.append(new_id)
                        entry["keyword"] = keyword
                        output.append(entry)
                    count += 1
    
    # clean up final output to help reduce token count and only keep the information that matters
    keys_to_remove = {'id', 'source', 'title'}
    filtered_data = [{k: v for k, v in d.items() if k not in keys_to_remove} for d in output]
    for item in filtered_data:
        date = f"{datetime.datetime.utcfromtimestamp(item['recorded']).strftime('%Y-%m-%d %H:%M:%S')} UTC"
        del item['recorded']
        item["date"] = date
    
    return filtered_data


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
