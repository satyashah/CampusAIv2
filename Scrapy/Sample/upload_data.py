import time
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import json
import re
import os

def fix_relative_links(data, base_url):
    # Parse the JSON string into a Python dictionary

    # Define a regex pattern to match relative links
    pattern = r'\(/(.*?)\)'

    # Function to replace relative links with absolute links
    def replace_relative_link(match):
        relative_path = match.group(1)
        absolute_link = f"{base_url}/{relative_path}"
        return f"({absolute_link})"

    # Iterate through the dictionary and replace relative links
    for key, value in data.items():
        if isinstance(value, list):
            for i, text in enumerate(value):
                # Use regex to find and replace relative links
                fixed_text = re.sub(pattern, replace_relative_link, text)
                value[i] = fixed_text

    return data

def add_random_texts_with_embeddings(collection, model, sample_texts, page_url):
    start_time = time.time()

    # print("Computing embeddings...")
    embeddings = model.encode(sample_texts)
    embedding_time = time.time() - start_time
    # print(f"Embeddings computed in {embedding_time:.2f} seconds.")

    # print("Preparing data for insertion...")
    data_to_insert = [
        {"text": text, "url": page_url, "plot_embedding": emb.tolist()} for text, emb in zip(sample_texts, embeddings)
    ]

    # print("Inserting data into MongoDB...")
    collection.insert_many(data_to_insert)
    total_time = time.time() - start_time
    print(f"Inserted texts with embeddings into MongoDB in {total_time:.2f} seconds.")

mongo_conn_string = "mongodb+srv://sshah132:Satya1234@cluster0.yeud864.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(mongo_conn_string)
db = client.testing
collection = db.samples

# Get all file names from the directory
data_dir = #r"C:\Programming\CampusAI\Scrapy\umd_scraper\scraped_data"
file_names = [f for f in os.listdir(data_dir) if f.endswith('.json')]

# Iterate through each file
for file_name in file_names:
# Load data from output.json
    print(f"Reading data from {file_name}...")
    with open(f"{data_dir}\\{file_name}") as f:
        data = json.load(f)

    data = fix_relative_links(data, "https://registrar.umd.edu")
    # Get the content from the first key from the array
    page_url = list(data.keys())[0]
    sample_texts = data[page_url]
    print(f"Inserting {len(sample_texts)} documents into MongoDB...")

    # Create a SentenceTransformer model
    model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

    # Call the function to add random texts with embeddings
    add_random_texts_with_embeddings(collection, model, sample_texts, page_url)