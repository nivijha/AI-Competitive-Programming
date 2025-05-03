import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Download required datasets (Run once)
nltk.download("stopwords")
nltk.download("wordnet")

# Sample data (Replace this with your dataset)
problems = [
    "Binary Search is an efficient search algorithm.",
    "Dijkstra's Algorithm finds the shortest path in a graph.",
    "The Fibonacci sequence appears in nature frequently!",
    "Implement Two Sum using a hashmap for efficiency."
]

# Initialize tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))
tokenizer = RegexpTokenizer(r'\w+')  # Tokenizes words only (no punctuation)

def preprocess_text(text):
    # Lowercase text
    text = text.lower()
    # Tokenize text (avoiding punkt)
    words = tokenizer.tokenize(text)
    # Remove stopwords and lemmatize
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    return " ".join(words)

# Apply preprocessing
cleaned_problems = [preprocess_text(problem) for problem in problems]

# TF-IDF transformation
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(cleaned_problems)

# Print results
print("Cleaned Data:", cleaned_problems)
print("\nTF-IDF Matrix:")
print(tfidf_matrix.toarray())
