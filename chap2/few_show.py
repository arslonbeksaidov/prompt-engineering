from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

# Start a conversation
messages = [
    {"role": "system", "content": "You are a helpful AI tutor that explains Python concepts clearly."}
]

# ---- Turn 1 ----
messages.append({"role": "user", "content": "What is a neural network?"})

response = client.chat.completions.create(
    model="gpt-5",
    messages=messages
)
answer = response.choices[0].message.content
print("Assistant:", answer)

# Save assistant reply
messages.append({"role": "assistant", "content": answer})

# ---- Turn 2 ----
messages.append({"role": "user", "content": "Can you show me a simple example using PyTorch?"})

response = client.chat.completions.create(
    model="gpt-5",
    messages=messages
)
answer = response.choices[0].message.content
print("Assistant:", answer)
