import requests
import json

# Set up the base URL for local Ollama API
url = "http://localhost:11434/api/chat"

# Define payload(your input prompt)
payload = {
    "model": "mistral", 
    "messages": [{"role": "user", "content": "What is Python?"}]
}

# Send HTTP POST request with stremaing enabled
response = requests.post(url, json=payload, stream=True)
# streaming mode lets us see the responses in real-time.

# Check response status
if response.status_code == 200:
    print("Streaming response from Ollama:")
    for line in response.iter_lines(decode_unicode=True):
        if line: # ignore empty lines
            try:
                # Parse each line as a JSON object
                json_data = json.loads(line)
                # Extract and print the message content
                if "message" in json_data and "content" in json_data["message"]:
                    print(json_data["message"]["content"], end="")
            except json.JSONDecodeError:
                print(f"\nFailed to parse line: {line}")
    # ensure final output ends with a new line
    print()

else:
    print(f"Error: {response.status_code}")
    print(response.text)
                    