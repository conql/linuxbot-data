from sentence_transformers import SentenceTransformer
import pandas as pd
from tqdm import tqdm

file_path = r"data\questions\500.csv"
save_path = r"data\questions\500_embed.csv"
col_name = "question"

df = pd.read_csv(file_path, encoding="utf-8-sig")
model = SentenceTransformer("BAAI/bge-small-zh")


embeddings = []
for i in tqdm(range(len(df))):
    embedding = model.encode(df.loc[i, col_name], normalize_embeddings=True)
    embeddings.append(embedding)

df["embedding"] = embeddings

df.to_csv(save_path, index=False, encoding="utf-8-sig")
