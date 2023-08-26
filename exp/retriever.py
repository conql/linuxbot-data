from annoy import AnnoyIndex
import pandas as pd
import transformers
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import json


class Retriever:
    def __init__(self):
        self.model = SentenceTransformer("BAAI/bge-small-zh")
        self.k_ann = AnnoyIndex(512, "angular")
        self.k_ann.load("data/knowledge.ann")
        self.q_ann = AnnoyIndex(512, "angular")
        self.q_ann.load("data/questions.ann")
        self.data = pd.read_csv("data/knowledge.csv", encoding="utf-8-sig")

    def embed(self, sentence):
        embedding = self.model.encode(sentence, normalize_embeddings=True)
        return embedding

    def search_by_content(self, question, top=10, threshold=0.5):
        question_embedding = self.embed(question)
        ids, distances = self.k_ann.get_nns_by_vector(
            question_embedding, top, include_distances=True
        )

        results = []
        for i, distance in zip(ids, distances):
            if distance > threshold:
                break
            results.append(self.data.loc[i, "content"])

        return results

    def search_by_question(self, question, top=10, threshold=0.5):
        question_embedding = self.embed(question)
        ids, distances = self.q_ann.get_nns_by_vector(
            question_embedding, top, include_distances=True
        )

        results = []
        for i, distance in zip(ids, distances):
            if distance > threshold:
                break
            results.append(self.data.loc[i, "content"])

        return results
