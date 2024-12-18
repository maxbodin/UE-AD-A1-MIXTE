import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Fonction permettant d'effectuer des requêtes GraphQL
def call_graphql_service(port, query, variables=None, headers=None):
    url = f'http://localhost:{port}/graphql'
    headers = headers or {}
    response = requests.post(url=url, json={"query": query, "variables": variables}, headers=headers) 
    return response