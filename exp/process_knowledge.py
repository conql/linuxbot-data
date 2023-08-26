import re
import numpy as np
import pandas as pd
import transformers
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import json
from sort_embed import sort_by_embedding_column
from annoy import AnnoyIndex


def build_tree():
    model = SentenceTransformer("BAAI/bge-small-zh")
    k_ann = AnnoyIndex(512, "angular")
    q_ann = AnnoyIndex(512, "angular")
    data = pd.read_csv("data/knowledge/train.csv", encoding="utf-8-sig")

    if "embedding" not in data.columns:
        data["embedding"] = None

    for i in tqdm(range(len(data))):
        k_embedding = model.encode(data.loc[i, "content"], normalize_embeddings=True)
        data.at[i, "embedding"] = k_embedding

        id = data.loc[i, "id"]
        k_ann.add_item(id, k_embedding)

        # example questions for retrieval
        questions = json.loads(data.loc[i, "questions"])
        for question in questions:
            q_embedding = model.encode(question, normalize_embeddings=True)
            q_ann.add_item(id, q_embedding)

    k_ann.build(10)
    k_ann.save("data/knowledge.ann")
    q_ann.build(10)
    q_ann.save("data/questions.ann")

    data = sort_by_embedding_column(data)
    data.to_csv("data/knowledge.csv", index=False, encoding="utf-8-sig")


def parse_answer(response):
    # Split the answer into sections
    sections = re.split(r"#\s*(\w+)", response)

    # Initialize a dictionary to hold the parsed answer
    parsed_answer = {}

    # Iterate over the sections
    for i in range(1, len(sections), 2):
        # Get the section title
        title = sections[i]

        # Get the section content
        content = sections[i + 1].strip()

        content = content.strip()
        if content.startswith("：") or content.startswith(":"):
            content = content[1:]
        content = content.strip()

        parsed_answer[title] = content

    knowledge_points = re.findall(
        r"【(.*?)】(.*?)(?=【|$)", parsed_answer["知识点"], re.DOTALL
    )
    if len(knowledge_points) == 0:
        raise Exception("No knowledge points found")
    parsed_answer["知识点"] = [
        {"title": kp[0], "content": re.sub(r"^\s*[：\:]", "", kp[1]).strip()}
        for kp in knowledge_points
    ]

    return parsed_answer


def extract_knowledge():
    df = pd.read_csv("data/questions/train.csv", encoding="utf-8-sig")
    k_df = pd.DataFrame(columns=["id", "title", "content", "questions"])
    for index, row in tqdm(df.iterrows(), total=len(df)):
        knowledge = json.loads(row["knowledge"])
        for kp in knowledge:
            k_df.loc[len(k_df)] = {
                "id": hash(kp["content"]) % (10**8),
                "title": kp["title"],
                "content": kp["content"],
                "questions": json.dumps([row["question"]]),
            }

    k_df.to_csv("data/knowledge/train.csv", index=False, encoding="utf-8-sig")


# if __name__ == "__main__":
#     path = r"data\questions\test.csv"
#     df = pd.read_csv(path)

#     df["knowledge"] = None
#     df["analysis"] = None

#     for index, row in df.iterrows():
#         try:
#             parsed = parse_answer(row["response"])
#             df.at[index, "knowledge"] = json.dumps(parsed["知识点"], ensure_ascii=False)
#             df.at[index, "analysis"] = parsed["分析"]

#         except Exception as e:
#             print(f"Error parsing question {index}: {e}")

#     df.to_csv(path, index=False, encoding="utf-8-sig")

if __name__ == "__main__":
    extract_knowledge()
    build_tree()
