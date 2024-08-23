import requests

url_to_call = "http://localhost:8000/work/"
response = requests.get(url_to_call)

if response.status_code == 200:
    # Handle the response data here
    print("Successfully called the URL!")
else:
    print(f"Error calling the URL (status code: {response.status_code})")