import os
import requests

from openai import OpenAI
from bs4 import BeautifulSoup

from src.scripts.vg.scraping import get_text_from_url, get_text_from_rss

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_completion(prompt, model = "gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return response.choices[0].message.content


def get_prompt_from_template(prompt_template, prompt_parameters):
    """
    Fills prompt parameters in prompt template and returns the generated prompt string

    :param prompt_template (str): The variables should be named var1, var2 etc. in the prompt_template
    :param prompt_parameters (List): List of variables. The length of this list should be the same as the number of vars in prompt_template

    :return: Returns prompt string with vars replaced by their values
    """
    prompt = prompt_template
    for i in range(len(prompt_parameters)):
        var_i = f"var{i}"
        prompt = prompt.replace(var_i, prompt_parameters[i])
    return prompt


def get_llm_response_from_url(url, prompt_template):

    # Get the prompt parameters by scraping the url
    url_text = get_text_from_rss(url)
    prompt_parameters = [url_text]

    # Fill the prompt_template to create the prompt
    prompt = get_prompt_from_template(prompt_template=prompt_template, prompt_parameters=prompt_parameters)

    # Query LLM to get response
    response = get_completion(prompt=prompt)

    return response


if __name__ == "__main__":

    news_link = f"""
    https://www.moneycontrol.com/india/newsarticle/rssfeeds/rssfeeds.php
    """

    prompt_template = f"""
    What impact do you think that the news article in the text below in triple backticks will have on the share price of ITC? 
    News article text: ```var1```
    """

    response = get_llm_response_from_url(news_link, prompt_template)
    print(response)