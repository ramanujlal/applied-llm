import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_completion(prompt, model = "gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].messages["content"]

prod_review = f"""
Needed a nice lamp for my bedroom, and this one had additional storage and not too high of a price point. \
Got it fast. The string to our lamp broke during the transit and the company happily sent over a new one. \
Came within a few days as well. It was easy to put together. \
Lumina seems to be a great company that cares about their customers and products.
"""

prompt = f"""
What is the sentiment of the following product review which is delimited by triple backticks? 
Give you answer as single word, either "positive" or "negative".

Review: '''{prod_review}'''
"""

response = get_completion(prompt)
print(response)