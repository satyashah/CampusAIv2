from trafilatura import fetch_url, extract
from sentence_transformers import SentenceTransformer
from nltk.tokenize import word_tokenize
import time
from pymongo import MongoClient
import json
import re
import os
#import nltk
# nltk.download('punkt')

# Specify the URL
url = 'https://registrar.umd.edu/calendars/standard-registration-dates-deadlines?field_academic_terms_target_id=401'

# Fetch the URL content
downloaded = fetch_url(url)

# Extract information from the HTML
result = extract(downloaded,output_format="txt", include_links=True, include_tables=True, favor_recall=True)


# Assuming 'result' contains the content of your text file
lines = result.split('\n')

# Initialize variables for grouping
groups = []
current_group = []
current_tokens = 0

# Iterate through each line
for line in lines:
    # Tokenize the line
    line = line.encode("ascii", "ignore").decode()
    tokens = word_tokenize(line)
    # Check if adding this line would exceed 700 tokens
    if current_tokens + len(tokens) > 700:
        # Start a new group if adding this line would exceed 700 tokens
        groups.append(current_group)
        current_group = [line]
        current_tokens = len(tokens)
    else:
        # Otherwise, add the line to the current group
        current_group.append(line)
        current_tokens += len(tokens)

# Append the last group if it's not empty
if current_group:
    groups.append(current_group)

# Convert all groups into one json file
group_arr = []
for group in groups:
    group_arr.append(" ".join(group))

json_file = {f"{url}": group_arr}

# ------------------------------------------------------------------------------------------------------------

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

data = fix_relative_links(json_file, "https://registrar.umd.edu")
# Get the content from the first key from the array
page_url = list(data.keys())[0]
sample_texts = data[page_url]
print(f"Inserting {len(sample_texts)} documents into MongoDB...")

# Create a SentenceTransformer model
model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")

# Call the function to add random texts with embeddings
add_random_texts_with_embeddings(collection, model, sample_texts, page_url)