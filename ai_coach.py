import openai

# Simple prompt for a title/caption suggestion
openai.api_key = input("Enter your OpenAI API Key: ")

while True:
    prompt = input("Enter mood or content to caption: ")
    if not prompt:
        break
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Give a mature, audience-friendly caption for: {prompt}",
        max_tokens=60,
        temperature=0.7,
    )
    print("Caption:", completion.choices[0].text.strip())