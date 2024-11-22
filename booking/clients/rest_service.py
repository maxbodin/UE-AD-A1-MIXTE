import os
import sys
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Fonction permettant d'effectuer les requêtes REST
def call_rest_service(port, endpoint, method='GET', data=None, headers=None):
    url = f'http://localhost:{port}/{endpoint}'  # Complete URL for the REST service
    headers = headers or {}
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")

        # Check if the response is empty or not valid JSON
        if response.status_code != 200:
            return {'error': f"Received a non-200 status code: {response.status_code}"}

        # Attempt to parse the response as JSON
        try:
            return response.json()
        except ValueError:
            # Handle non-JSON response
            return {'error': "Failed to parse response as JSON."}

    except requests.RequestException as e:
        return {'error': str(e)}