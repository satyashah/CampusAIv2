from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
import re

app = Flask(__name__)
CORS(app)

client = OpenAI(
    # This is the default and can be omitted
    api_key= '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',
)

def query_embeddings_with_vector_search(query_text):
    mongo_conn_string = "mongodb+srv://sshah132:Satya1234@cluster0.yeud864.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(mongo_conn_string)

    model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")
    db = client.testing
    collection = db.samples


    query_embedding = model.encode([query_text])[0].tolist()

    print("Executing vector search...")
    pipeline = [
    {
        '$vectorSearch': {
        'index': 'default', 
        'path': 'plot_embedding', 
        'queryVector': query_embedding,
        'numCandidates': 150, 
        'limit': 3
        }
    }, {
        '$project': {
        '_id': 0, 
        'plot': 1, 
        'text': 1, 
        'url': 1,
        'score': {
            '$meta': 'vectorSearchScore'
        }
        }
    }
    ]

    results = list(collection.aggregate(pipeline))
    return results

def text_processing(text):

    # text = re.sub(r'^- (.*)', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*-\s+(.*)', r'<li>\1', text, flags=re.MULTILINE)

    # Convert Markdown-like bold text to HTML underline
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<u>\1</u>', text)

    # Convert Markdown-like bold text to HTML bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Convert Markdown-like headings to HTML headings
    text = re.sub(r'### (.*?)\n', r'<h3>\1</h3>\n', text)
    
    # Convert Markdown-like links to HTML links
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    
    # Replace newlines with <br> tags
    text = text.replace('\n', '<br>')
    
    return text

@app.route('/askGPT', methods=['POST'])
def process_text():
    data = request.get_json()
    input_text = data.get('content', '')
    print(input_text)

    prev = input_text['messages']
    if len(prev) >= 2:
        query = input_text['inputValue'] + ", " + prev[-2]['text']
    else:
        query = input_text['inputValue']

    context = query_embeddings_with_vector_search(query)
    # Loop through the results and extract the text
    context_text = ""
    links = ""
    for doc in context:
        links += f"{doc['url']}, "
        context_text += doc['text'] + " "
    
    if len(prev) >= 2:
        messages=[
            {
                "role": "system",
                "content": "You are an AI academic advisor at UMD. A student comes to you for advice.",
            },
            {
                "role": "system",
                "content": f"The last question the student asked was {prev[-2]['text']} and you responded with {prev[-1]['text']}",
            },
            {   
                "role": "user",
                "content": f"The student asks: {query}",
            },
            {
                "role": "system",
                "content": f"Based on the information provided, offer advice that is both relevant and actionable. Include any relevant website sources directly from the provided information such as {links}, do not provide any other links. Your response should be structured to provide clear, concise, and helpful information to the student.\n Here is the important information: {context_text}."
            },
        ]
    else:
        messages=[
            {
                "role": "system",
                "content": "You are an AI academic advisor at UMD. A student comes to you for advice.",
            },
            {   
                "role": "user",
                "content": f"The student asks: {query}",
            },
            {
                "role": "system",
                "content": f"Based on the information provided, offer advice that is both relevant and actionable. Include any relevant website sources directly from the provided information such as {links}. Your response should be structured to provide clear, concise, and helpful information to the student.\n Here is the important information: {context_text}."
            },
        ]

    print(messages)
    
    chat_completion = client.chat.completions.create(
        messages = messages,
        model="gpt-3.5-turbo",
    )

    # Extract the generated text from the response
    print(chat_completion)
    gptResponse = chat_completion.choices[0].message.content

    gptResponse = text_processing(gptResponse)

    return jsonify({'result': gptResponse})

if __name__ == '__main__':
    app.run(debug=True)
