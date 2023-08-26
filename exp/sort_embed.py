import torch
import pandas as pd
from tqdm import tqdm


def nearest_neighbor_chain_sort(vectors, use_gpu=False, normalize_vectors=True):
    # Ensure the vectors are in PyTorch tensor format
    if not isinstance(vectors, torch.Tensor):
        vectors = torch.tensor(vectors)

    # Move vectors to GPU if requested
    if use_gpu and torch.cuda.is_available():
        vectors = vectors.cuda()

    # Normalize the vectors if requested
    if normalize_vectors:
        vectors = torch.nn.functional.normalize(vectors, dim=1)

    # Compute cosine similarity matrix
    sim_matrix = torch.mm(vectors, vectors.t())

    # Start with the first vector
    index = 0
    sorted_indices = [index]

    # Use tqdm to show progress
    for _ in range(1, vectors.size(0)):
        # Set the similarity of the chosen vector to itself to a large negative value so it's not chosen again
        sim_matrix[index, index] = float("-inf")

        # Find the index of the vector that is most similar to the current one
        next_index = torch.argmax(sim_matrix[index]).item()
        
        # Set all similarities to the current vector to a large negative value so it's not chosen again
        sim_matrix[:, index] = float("-inf")
        index = next_index
        sorted_indices.append(index)

    print(sorted_indices)
    return sorted_indices


def sort_by_embedding_column(df, use_gpu=False, normalize_vectors=True):
    # Convert the embedding column to a list of tensors
    embeddings = (
        df["embedding"]
        .str.strip("[]")
        .str.split()
        .apply(lambda x: [float(i) for i in x])
        .tolist()
    )
    embeddings_tensor = torch.stack([torch.tensor(e) for e in embeddings])

    # Sort using the previous function
    sorted_embeddings = nearest_neighbor_chain_sort(
        embeddings_tensor, use_gpu, normalize_vectors
    )

    # Create a DataFrame from the sorted embeddings
    sorted_df = df.iloc[sorted_embeddings]

    return sorted_df


if __name__ == "__main__":
    df = pd.read_csv(r"data\questions\500_embed.csv", encoding="utf-8-sig")
    sorted_df = sort_by_embedding_column(df, use_gpu=True, normalize_vectors=False)
    sorted_df.to_csv(
        r"data\questions\500_embed_sorted.csv", index=False, encoding="utf-8-sig"
    )
