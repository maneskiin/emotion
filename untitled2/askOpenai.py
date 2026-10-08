from openai import OpenAI

openai_api_base = "http://10.108.16.44:8000" # /v1/chat/completions
client = OpenAI(
    api_key='EMPTY',
    base_url=openai_api_base,
)
models = client.models.list()
model = models.data[0].id
# completion = client.completions.create(model=model, prompt="hello")
# print("Completion result:", completion)




chat_response = client.chat.completions.create(
    model=model,
    messages=[
        # {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "hello"},
    ]
)
print("Chat response:", chat_response)

