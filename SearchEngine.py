import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the preprocessed problem statements
with open('cleaned_problems.json', 'r', encoding='utf-8') as f:
    cleaned_problems = json.load(f)

# Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(cleaned_problems)

# Function to search problems based on a user query
def search_problems(query, top_n=5):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    # Get indices of top_n most similar problems
    top_indices = similarities.argsort()[-top_n:][::-1]
    results = []
    for idx in top_indices:
        results.append({
            "problem": cleaned_problems[idx],
            "similarity_score": round(similarities[idx], 4)
        })
    return results

# Example usage
if __name__ == "__main__":
    user_query = input("🔍 Enter your search query: ")
    recommendations = search_problems(user_query, top_n=5)
    print("\n✅ Top matching problems:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['problem']} (Score: {rec['similarity_score']})")
