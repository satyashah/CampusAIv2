from trafilatura import fetch_url, extract
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk.tokenize import word_tokenize

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
    print(line)

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

#Write the json file
import json
with open('output.json', 'w') as f:
    json.dump(json_file, f)
