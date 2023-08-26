import pandas as pd
import json
import os
import re
import random

file_path = "./data/500题已回答.csv"
train_ratio = 0.9

file_name = os.path.splitext(os.path.basename(file_path))[0]

# Read in the data
df = pd.read_csv(file_path)

# Convert each row into a json object
rows = []
max_source_length = 0
max_target_length = 0
for index, row in df.iterrows():
    question = re.sub(r"\n正确答案[：:].*", "", row["Question"])
    sections = re.split(r"#\s*(\w+).*?\n", row["Response"])
    answer = ""

    if "知识点" in sections:
        question += f"\n\n已知：\n# 知识点：\n{sections[sections.index('知识点') + 1]}\n"

    if "分析" in sections:
        answer += f"# 分析：\n{sections[sections.index('分析') + 1]}\n"

    if "答案" in sections:
        answer += f"# 答案：\n{sections[sections.index('答案') + 1]}\n"
    else:
        raise Exception("No answer found")

    max_source_length = max(max_source_length, len(question))
    max_target_length = max(max_target_length, len(answer))

    if len(answer) >= max_target_length:
        print(answer)

    rows.append(
        json.dumps({"question": question, "answer": answer}, ensure_ascii=False)
    )

# Shuffle the rows
random.shuffle(rows)

# split train and dev
train_rows = rows[: int(len(rows) * train_ratio)]
dev_rows = rows[int(len(rows) * train_ratio) :]

if not os.path.exists(file_name):
    os.mkdir(file_name)

# Write the json to a file
with open(os.path.join(file_name, "train.json"), "w", encoding="utf-8") as f:
    f.write("\n".join(train_rows))

with open(os.path.join(file_name, "dev.json"), "w", encoding="utf-8") as f:
    f.write("\n".join(dev_rows))


print(f"max_source_length: {max_source_length}")
print(f"max_target_length: {max_target_length}")
