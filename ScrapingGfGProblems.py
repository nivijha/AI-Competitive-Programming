import requests
from bs4 import BeautifulSoup
import json

# URL of a GeeksforGeeks problem page (Change as needed)
BASE_URL = "https://www.geeksforgeeks.org/python-programming-examples/"

# Function to scrape problem titles and links
def scrape_problems():
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    problems = []

    # Find all problem links
    for link in soup.select("article a"):
        title = link.text.strip()
        url = link["href"]
        if "python-program" in url:  # Filter relevant URLs
            problems.append({"title": title, "url": url})

    return problems

# Function to scrape solution code from each problem page
def scrape_solution(problem_url):
    response = requests.get(problem_url)
    if response.status_code != 200:
        return "Solution not found"

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract code blocks from the page
    code_blocks = soup.find_all("pre")
    solutions = [block.text for block in code_blocks]

    return solutions if solutions else "Solution not found"

# Scrape all problems
problems = scrape_problems()

# Scrape solutions for the first 5 problems (for demo)
dataset = []
for problem in problems[:5]:
    print(f"Scraping: {problem['title']}")
    solutions = scrape_solution(problem["url"])
    dataset.append({"question": problem["title"], "code": solutions})

# Save dataset to a JSON file
with open("coding_dataset.json", "w") as f:
    json.dump(dataset, f, indent=4)

print("✅ Scraping complete! Dataset saved as 'coding_dataset.json'.")
