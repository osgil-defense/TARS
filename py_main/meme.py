import os
import requests
import json

def search_data(queries: list):
    """
    Search for key words in a cybersecurity news database hosted by Notify Cyber.

    Parameters:
        queries (list of str): List of keywords to search for from the API.

    Raises:
        ValueError: If queries is not a list of strings, or if any query is not a string.
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

    all_results = {}
    for query in queries:
        response = requests.get(
            f"https://nc-api.vercel.app/search?{query}",
            headers={"Authorization": auth_token},
        )
        if response.ok:
            all_results[query] = response.json()

    sourced_all_results = {}
    for key in all_results:
        if key not in sourced_all_results:
            sourced_all_results[key] = {}
        for entry in all_results[key]:
            source = entry["source"]
            if source not in sourced_all_results[key]:
                sourced_all_results[key][source] = []
            sourced_all_results[key][source].append(entry)

    n = 20
    output = []
    kn = int(n / len(sourced_all_results))
    for keyword in sourced_all_results:
        sn = int(kn / len(sourced_all_results[keyword])) or 1
        for source in sourced_all_results[keyword]:
            counter = 0
            for entry in sourced_all_results[keyword][source]:
                if counter < sn:
                    output.append(entry)
                counter += 1
    
    return output


if __name__ == "__main__":
    queries = ["gpt", "python", "Junos OS", "linux"]
    all_results = search_data(queries)
    print("--->", len(all_results))
    # print(json.dumps(all_results, indent=4))
