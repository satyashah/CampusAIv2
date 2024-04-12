import time
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient


def add_random_texts_with_embeddings(collection, model, sample_texts):
    print("Selecting random texts...")
    start_time = time.time()

    print("Computing embeddings...")
    embeddings = model.encode(sample_texts)
    embedding_time = time.time() - start_time
    print(f"Embeddings computed in {embedding_time:.2f} seconds.")

    print("Preparing data for insertion...")
    data_to_insert = [
        {"text": text, "plot_embedding": emb.tolist()} for text, emb in zip(sample_texts, embeddings)
    ]

    print("Inserting data into MongoDB...")
    collection.insert_many(data_to_insert)
    total_time = time.time() - start_time
    print(f"Inserted texts with embeddings into MongoDB in {total_time:.2f} seconds.")

# Example usage


# Add random texts with embeddings to the database

def query_embeddings_with_vector_search(query_text, collection, model):
    print("Embedding the query text...")
    start_time = time.time()
    query_embedding = model.encode([query_text])[0].tolist()

    print("Executing vector search...")
    pipeline = [
        {
            "$vectorSearch": {
                "index": "testingIndex", # The name of index to use for vector search
                "path": "plot_embedding", # The field that contains the embeddings
                "queryVector": query_embedding, # The query vector
                "numCandidates": 100, # Number of candidates to retrieve
                "limit": 3 # Limit the output to 3 results
            }
        },
        {
            "$project": {"_id": 0, "text": 1} # Shapes the output so no id, only shows text
        }
    ]

    results = list(collection.aggregate(pipeline))
    total_time = time.time() - start_time
    print(f"Vector search completed in {total_time:.2f} seconds.")
    return results

mongo_conn_string = "mongodb+srv://emenikeemail:Ninjaboy12345$@cluster0.wl4qsvv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_conn_string)
db = client.testing
collection = db.samples

model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

# Sample texts to choose from
sample_texts = [
    "A man is eating a piece of bread.",
    "A man is eating food.",
    "A man is eating pasta.",
    "The girl is carrying a baby.",
    "A man is riding a horse.",
    "The sky is clear tonight.",
    "She is reading a book.",
    "The car is moving fast."
]
add_random_texts_with_embeddings(collection, model, sample_texts)
query_text = "A man is eating a piece of paper like square food."
results = query_embeddings_with_vector_search(query_text, collection, model)
for doc in results:  # Display results
    print(doc)

