from dotenv import load_dotenv
import requests
import os
import json
from pprint import pprint
import time
import pandas as pd
from tqdm import tqdm

load_dotenv()
API_KEY = os.getenv("API_KEY")

def complete(messages):
    url = "https://chimeragpt.adventblocks.cc/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    data = {"model": "gpt-4", "messages": messages}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()  # This will raise an HTTPError if the response was an error
    return response.json()["choices"][0]["message"]["content"]


def answer(query: str):
    # Read the first user message from "prompt.txt"
    with open("prompt.txt", "r", encoding="utf-8") as file:
        first_user_message = file.read().strip()

    # Define the messages
    messages = [
        {
            "role": "system",
            "content": "You are GPT-4, a large language model trained by OpenAI. Carefully heed the user's instructions.",
        },
        {"role": "user", "content": first_user_message},
        {"role": "user", "content": query},
    ]

    # Call the complete function and return the response
    return complete(messages)


def load_data(path: str):
    # Open the file and read its content
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    # Split the content by "\n\n" and return the result
    return content.split("\n\n")


def get_answers_and_save(data, output_file, wait_time=10):
    # Try to load the existing DataFrame from the CSV file
    try:
        df = pd.read_csv(output_file, encoding="utf-8-sig")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Question", "Response"])

    # Determine where to resume from
    start_index = len(df)

    for question in tqdm(data[start_index:]):
        start_time = time.time()

        response = None
        while response is None:
            try:
                # Get the answer for the current question
                response = answer(question)
            except Exception as e:
                print(e)
                print("Retrying in 10 seconds...")
                time.sleep(10)

        # Append the question and response to the DataFrame
        df.loc[len(df)] = {"Question": question, "Response": response}  # type: ignore

        df.to_csv(output_file, index=False, encoding="utf-8-sig")

        processing_time = time.time() - start_time
        # If it took less than wait_time seconds, wait for the remaining time
        if processing_time < wait_time:
            time.sleep(wait_time - processing_time)


if __name__ == "__main__":
    data = load_data("data/课后测验.txt")
    get_answers_and_save(data, "data/课后测验.csv")
