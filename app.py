from flask import Flask, request, jsonify
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load the cleaned problems
with open('cleaned_problems.json', 'r', encoding='utf-8') as f:
    cleaned_problems = json.load(f)

# Initialize vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(cleaned_problems)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "No query provided"}), 400

    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = similarities.argsort()[-5:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            "problem": cleaned_problems[idx],
            "similarity_score": round(similarities[idx], 4)
        })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
