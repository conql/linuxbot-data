import json
import pandas as pd

with open("data/generated_predictions.json", "r", encoding="utf-8") as file:
    content = file.readlines()
data = [json.loads(line) for line in content]

df = pd.DataFrame(columns=["labels", "predict"])
for item in data:
    df.loc[len(df)] = {
        "labels": item["labels"],
        "predict": item["predict"],
    }
df.to_csv("data/generated_predictions.csv", index=False, encoding="utf-8-sig")