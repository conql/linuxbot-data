import json
import re
import pandas as pd
import os
from tqdm import tqdm
import time
import requests
import math


def load_trainset(path):
    with open(path, "r", encoding="utf-8") as file:
        content = file.readlines()
    return [json.loads(line) for line in content]


def init(result_path, trainset_path):
    if os.path.exists(result_path):
        return pd.read_csv(result_path, encoding="utf-8-sig")

    # create a dataframe
    df = pd.DataFrame(columns=["Question", "Answer", "Response"])
    trainset = load_trainset(trainset_path)
    for item in trainset:
        df.loc[len(df)] = {
            "Question": item["question"],
            "Answer": item["answer"],
            "Response": "",
        }
    df.to_csv(result_path, index=False, encoding="utf-8-sig")
    return df


last_call_time = 0


def infer(question, interval=3):
    global last_call_time
    time.sleep(max(0, interval - (time.time() - last_call_time)))
    last_call_time = time.time()

    resp = requests.post(
        "http://localhost:8000/api/generate",
        json={
            "messages": [
                {
                    "role": "user",
                    "content": question,
                }
            ]
        },
    )

    text = resp.text
    attachs, cleaned_text = extract_attach_list(text)
    attach_str = "\n".join([f'{a["title"]}\n{a["content"]}' for a in attachs])

    return attach_str + "\n" + cleaned_text


def extract_attach_list(message: str):
    regex = re.compile(r"```attachment\n([\s\S]*?)\n```", re.MULTILINE)

    attachments = []
    cleaned_string = message
    matches = regex.findall(message)

    for match in matches:
        try:
            attach = json.loads(match)
        except json.JSONDecodeError:
            attach = {
                "type": "text",
                "title": "error",
                "content": f"Malformed attachment{match}",
            }
        attachments.append(attach)
        cleaned_string = cleaned_string.replace(f"```attachment\n{match}\n```", "")

    return attachments, cleaned_string


if __name__ == "__main__":
    result_path = r"data/evalue.csv"
    trainset_path = r"data\LinuxBot\dev.json"

    resume = input("Resume? (y/n) ") == "y"
    if not resume:
        if os.path.exists(result_path):
            os.remove(result_path)
    df = init(result_path, trainset_path)

    # for every question in trainset
    for index, row in tqdm(df.iterrows(), total=len(df)):
        if isinstance(row["Response"], str) and row["Response"].strip() != "":
            continue
        response = infer(row["Question"])
        df.loc[index, "Response"] = response
        df.to_csv(result_path, index=False, encoding="utf-8-sig")
