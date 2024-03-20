import time
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim

# Start measuring time for model loading
start_load_time = time.time()

print("loading model")
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")
print("model loaded")

# Measure and print the time taken to load the model
load_time = time.time() - start_load_time
print(f"Time taken to load model: {load_time:.2f} seconds")

# For retrieval you need to pass this prompt.
query = 'Represent this sentence for searching relevant passages: A man is eating a piece of bread' # Do we need the first half?

docs = [
    query,
    "A man is eating food.",
    "A man is eating pasta.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
]

# Start measuring time for encoding
start_encode_time = time.time()

print("encoding")
embeddings = model.encode(docs)
print("encoded")

# Measure and print the time taken to encode the documents
encode_time = time.time() - start_encode_time
print(f"Time taken to encode documents: {encode_time:.2f} seconds")

# Calculate cosine similarity
similarities = cos_sim(embeddings[0], embeddings[1:])
print(similarities)
