# Install: pip install requests
import requests
import time
import webbrowser

# 1) Initiate device authorization
device_url = "https://auth.konnektr.io/oauth/device/code"
device_data = {
    "client_id": "14xWhGB5yYyyzdOHqjOjAl0KOU6e6UbF",
    "scope": "openid profile email",
    "audience": "https://graph.konnektr.io",
}
device_response = requests.post(device_url, json=device_data)
device_info = device_response.json()

print(f"Please visit: {device_info['verification_uri_complete']}")
print(
    f"Or go to {device_info['verification_uri']} and enter: {device_info['user_code']}"
)

# Optionally open browser
webbrowser.open(device_info["verification_uri_complete"])

# 2) Poll for token
token_url = "https://auth.konnektr.io/oauth/token"
token_data = {
    "client_id": "14xWhGB5yYyyzdOHqjOjAl0KOU6e6UbF",
    "device_code": device_info["device_code"],
    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
}

while True:
    token_response = requests.post(token_url, json=token_data)
    token_result = token_response.json()

    if "error" in token_result:
        if token_result["error"] == "authorization_pending":
            print("Waiting for authentication...")
            time.sleep(5)
        else:
            raise Exception(f"Error: {token_result['error']}")
    else:
        access_token = token_result["access_token"]
        print("Authentication successful!")
        break

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

# 3) Use the token
query_url = "https://resource-id.api.graph.konnektr.io/query"
query_payload = {"query": "SELECT * FROM digitaltwins"}
query_response = requests.post(query_url, json=query_payload, headers=headers)
print(query_response.json())
