# pip install ollama
import ollama 

# Initialize the Ollama client
client = ollama.Client()

# Define model and input prompt
model = "llama3"
prompt = "What is Python?"


# Send query to model
response = client.generate(model=model, prompt=prompt)


# Print response from model
print("Response from Ollama:")
print(response.response)