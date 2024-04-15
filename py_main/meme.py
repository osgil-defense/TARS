import datetime
import os
import requests
import json

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

if __name__ == "__main__":
    queries = ["gpt", "python", "Junos OS", "linux", "atom"]
    all_results = search_data(queries)
    print(json.dumps(all_results, indent=4))
    print("--->", len(all_results))
