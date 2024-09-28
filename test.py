import requests
import json

# Define the base URL and API key
base_url = "https://berrydisco.openai.azure.com/"
api_key = "0c115be8ffff4e53a79c3cbbd0662b90"

# Define the endpoint for completions
endpoint = base_url + "openai/deployments/YOUR_DEPLOYMENT_NAME/completions?api-version=2022-12-01"

# Define the headers with the API key
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Define the payload (example request body for completions)
payload = {
    "prompt": "Once upon a time,",
    "max_tokens": 50
}

# Send a POST request to the completions endpoint
response = requests.post(endpoint, headers=headers, json=payload)

# Check for success
if response.status_code == 200:
    # Print the response JSON if successful
    result = response.json()
    print(json.dumps(result, indent=2))
else:
    # Print the error message if request fails
    print(f"Error: {response.status_code} - {response.text}")
