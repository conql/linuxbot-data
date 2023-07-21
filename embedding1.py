import os
from tqdm import tqdm
import requests
import json
import pandas as pd
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_embedding(text):
    # Define the API endpoint
    url = "https://chimeragpt.adventblocks.cc/v1/embeddings"

    # Define the headers for the API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Define the data for the API request
    data = {"model": "text-embedding-ada-002", "input": text}

    # Make the API request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the embedding from the response
        embedding = response.json().get("data")[0].get("embedding")
        return embedding
    else:
        print(f"Request failed with status code {response.status_code}")
        return None


def main():
    # Load the CSV file
    df = pd.read_csv("knowledge_points.csv", encoding="utf-8-sig")

    # Check if 'embedding' column exists, if not, create it
    if "embedding" not in df.columns:
        df["embedding"] = None

    # Define the maximum number of requests per minute
    max_requests_per_minute = 40

    # Calculate the delay between requests
    delay = 60 / max_requests_per_minute

    # Get the embeddings for each combined text
    for i in tqdm(df.index):
        # Skip rows that have already been processed
        if pd.notna(df.at[i, "embedding"]):
            continue

        # Combine the 'title' and 'content' fields temporarily
        text = "【" + df.at[i, "title"] + "】" + df.at[i, "content"]

        start_time = time.time()
        embedding = get_embedding(text)
        end_time = time.time()

        # Retry failed requests
        retry_count = 0
        while embedding is None and retry_count < 3:
            print(f"Retrying request for row {i}...")
            embedding = get_embedding(text)
            retry_count += 1
            time.sleep(delay)

        df.at[i, "embedding"] = embedding

        # Save the DataFrame back to a CSV file
        df.to_csv("knowledge_points.csv", index=False, encoding="utf-8-sig")

        elapsed_time = end_time - start_time
        if elapsed_time < delay:
            time.sleep(delay - elapsed_time)

    # Convert the DataFrame to a JSON object
    data = df.to_dict("records")
    data = [
        {
            "title": row["title"],
            "content": row["content"],
            "vector": json.loads(row["embedding"]),
        }
        for row in data
    ]
    json_obj = {"rows": data}

    # Save the JSON object as a JSON file
    with open("knowledge_points.json", "w", encoding="utf-8") as f:
        json.dump(json_obj, f, ensure_ascii=False)


if __name__ == "__main__":
    main()
