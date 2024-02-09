import requests

# Define the Context Broker base URL
context_broker_url = "http://150.140.186.118:1026/v2/entities"

# Define the entity ID you want to delete
entity_id_to_delete = "urn:ngsild:Vehicle:Bus:5"

# Define the entity type you want to delete
entity_type_to_delete = "Vehicle"

# Construct the URL for the specific entity
delete_url = f"{context_broker_url}/{entity_id_to_delete}?type={entity_type_to_delete}"

# Define headers (optional, but recommended)
headers = {"Accept": "application/json"}

# Send the DELETE request without setting the Content-Type header
response = requests.delete(delete_url, headers=headers)

# Check the response status
if response.status_code == 204:
    print(f"Entity {entity_id_to_delete} of type {entity_type_to_delete} deleted successfully.")
else:
    print(f"Failed to delete entity. Status code: {response.status_code}")
    print(response.text)