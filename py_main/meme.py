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
    if not isinstance(queries, list) or not all(isinstance(query, str) for query in queries):
        raise ValueError("Queries must be a list of strings")

    auth_token = os.getenv("NC_API_TOKEN")
    if not auth_token:
        raise ValueError("NC_API_TOKEN environment variable is not set")

    query_string = ",".join(queries)
    url = f"https://nc-api.vercel.app/search?{query_string}"
    response = requests.get(url, headers={"Authorization": auth_token})
    if response.ok:
        return response.json()
    else:
        raise Exception(f"Failed to search: {response.status_code} - {response.text}")

def reciprocal_rank_fusion(all_results):
    """
    Combines search results from multiple queries using reciprocal rank fusion.

    Parameters:
        all_results (dict): Dictionary where keys are queries and values are lists of document dicts.

    Returns:
        Dictionary where keys are queries and values are sorted lists of document dicts based on rank fusion.
    """
    fused_scores = {}
    query_details = {}

    # Calculate scores for each document across all queries
    for query, results in all_results.items():
        for index, doc in enumerate(results):
            doc_id = doc['id']
            if doc_id not in fused_scores:
                fused_scores[doc_id] = {'score': 0, 'details': doc}
                query_details[doc_id] = [query]
            else:
                query_details[doc_id].append(query)
            fused_scores[doc_id]['score'] += 1 / (index + 1)  # Simple reciprocal rank scoring

    # Organize documents back into a dictionary based on the query
    final_results = {query: [] for query in all_results.keys()}
    for doc_id, info in fused_scores.items():
        for query in query_details[doc_id]:
            final_results[query].append(info['details'])

    # Sort the documents for each query
    for query in final_results:
        final_results[query] = sorted(final_results[query], key=lambda x: fused_scores[x['id']]['score'], reverse=True)

    return final_results

if __name__ == "__main__":
    queries = ["gpt", "python"]  # Example set of queries
    all_results = {}
    for query in queries:
        search_results = search_data([query])
        all_results[query] = search_results

    reranked_results = reciprocal_rank_fusion(all_results)

    output = {
        "raw": all_results,
        "ranked": reranked_results
    }

    print(json.dumps(output, indent=4))
