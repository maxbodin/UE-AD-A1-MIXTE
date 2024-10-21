import requests

def call_graphql_service(port, query, variables=None, headers=None):
    url = f'http://localhost:{port}/graphql'  # Complete URL for the REST service
    headers = headers or {}

    response = requests.post(url=url, json={"query": query, "variables": variables}, headers=headers) 
    
    return response