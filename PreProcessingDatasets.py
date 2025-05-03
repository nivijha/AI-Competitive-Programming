import json
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer
import nltk

# Download required resources
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))
tokenizer = TreebankWordTokenizer()

# Function to preprocess text
def preprocess_text(text):
    # Tokenize the text (TreebankWordTokenizer doesn't need punkt)
    tokens = tokenizer.tokenize(text.lower())
    # Remove stopwords & punctuation, and lemmatize each word
    tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word not in stop_words and word not in string.punctuation
    ]
    return ' '.join(tokens)

# Load the combined problems JSON file
with open('combined_problems.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Prepare a list of problem texts (title + tags) safely
problems = []
for p in data.get('problems', []):
    title = p.get('title') or ''
    tags = p.get('tags') or []
    tags_text = ' '.join(tags) if isinstance(tags, list) else str(tags)
    full_text = f"{title} {tags_text}".strip()
    if full_text:  # Skip empty problems
        problems.append(full_text)

# Preprocess each problem description
cleaned_problems = [preprocess_text(p) for p in problems]

# Save the cleaned problems to a new JSON file
with open('cleaned_problems.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_problems, f, indent=2, ensure_ascii=False)

print(f"Preprocessed {len(cleaned_problems)} problems and saved to 'cleaned_problems.json'")
