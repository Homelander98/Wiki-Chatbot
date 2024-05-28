from flask import Flask, request, jsonify
import wikipediaapi
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

user_agent = 'Wikipedia-Chatbot/1.0 (https://yourwebsite.com/contact; your-email@example.com)'
wiki = wikipediaapi.Wikipedia('en', headers={'User-Agent': user_agent})

def get_summary(title):
    page = wiki.page(title)
    if page.exists():
        return page.summary
    else:
        return "Sorry, I couldn't find any information on that topic."

def get_infobox(title):
    page = wiki.page(title)
    if page.exists():
        return page.text
    else:
        return "Sorry, I couldn't find any information on that topic."

def handle_query(query):
    query = query.lower().strip()

    if query.startswith('tell me about '):
        topic = query[len('tell me about '):].strip()
        return get_summary(topic)

    elif query.startswith('infobox for '):
        topic = query[len('infobox for '):].strip()
        return get_infobox(topic)

    else:
        return "Sorry, I didn't understand that. You can ask me to 'tell me about [topic]' or 'infobox for [topic]'."

@app.route('/query', methods=['POST'])
def query():
    data = request.json
    query = data.get('query', '')
    response = handle_query(query)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(port=5000)
