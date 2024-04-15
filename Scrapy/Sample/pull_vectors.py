import time
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient


mongo_conn_string = "mongodb+srv://sshah132:Satya1234@cluster0.yeud864.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_conn_string)
db = client.testing
collection = db.samples


def query_embeddings_with_vector_search(query_text, collection, model):
    print("Embedding the query text...")
    start_time = time.time()
    query_embedding = model.encode([query_text])[0].tolist()

    print("Executing vector search...")
    pipeline = [
    {
        '$vectorSearch': {
        'index': 'default', 
        'path': 'plot_embedding', 
        'queryVector': query_embedding,
        'numCandidates': 150, 
        'limit': 2
        }
    }, {
        '$project': {
        '_id': 0, 
        'plot': 1, 
        'text': 1, 
        'score': {
            '$meta': 'vectorSearchScore'
        }
        }
    }
    ]

    results = list(collection.aggregate(pipeline))
    total_time = time.time() - start_time
    print(f"Vector search completed in {total_time:.2f} seconds.")
    return results

# Create a SentenceTransformer model
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

query_text = "Do I need to submit the writing portion of the SAT?"
results = query_embeddings_with_vector_search(query_text, collection, model)
print("Results:", results)
for doc in results:  # Display results
    print(doc)
 