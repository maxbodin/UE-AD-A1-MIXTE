from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from con

def call_graphql_service(port, query, variables=None):
    transport = RequestsHTTPTransport(
        url = f'http://localhost:{port}/graphql',
        use_json=True,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)
    response = client.execute(gql(query), variable_values=variables)
    return response