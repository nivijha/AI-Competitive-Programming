import requests
import csv
import json
from time import sleep
from random import randint

# Configure settings
API_URL = "https://leetcode.com/graphql"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
BATCH_SIZE = 50  # Number of problems to fetch per request
TOTAL_PROBLEMS = 1000  # Adjust based on how many you want
OUTPUT_CSV = "leetcode_problems.csv"
OUTPUT_JSON = "leetcode_problems.json"

# GraphQL query with pagination
QUERY = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
  problemsetQuestionList: questionList(
    categorySlug: $categorySlug
    limit: $limit
    skip: $skip
    filters: $filters
  ) {
    total: totalNum
    questions: data {
      questionId
      frontendQuestionId: questionFrontendId
      title
      titleSlug
      difficulty
      acRate
      isPaidOnly
      topicTags {
        name
        slug
      }
      hasSolution
      hasVideoSolution
    }
  }
}
"""

def fetch_problems(limit, skip):
    variables = {
        "categorySlug": "",
        "skip": skip,
        "limit": limit,
        "filters": {}
    }
    
    try:
        response = requests.post(
            API_URL,
            json={"query": QUERY, "variables": variables},
            headers=HEADERS
        )
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            print(f"GraphQL Errors at skip {skip}:")
            for error in data["errors"]:
                print(f"- {error['message']}")
            return None
        
        return data["data"]["problemsetQuestionList"]["questions"]
    
    except Exception as e:
        print(f"Error fetching problems (skip {skip}): {str(e)}")
        return None

def create_dataset():
    all_problems = []
    skip = 0
    
    while len(all_problems) < TOTAL_PROBLEMS:
        print(f"Fetching problems {skip} to {skip+BATCH_SIZE-1}...")
        
        problems = fetch_problems(BATCH_SIZE, skip)
        if not problems:
            break
        
        all_problems.extend(problems)
        skip += BATCH_SIZE
        
        # Respectful delay between requests
        sleep(randint(1, 3))
        
        # Early exit if we've fetched all available problems
        if len(problems) < BATCH_SIZE:
            break
    
    print(f"\nTotal problems fetched: {len(all_problems)}")
    return all_problems

def save_to_csv(problems, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            'questionId',
            'frontendQuestionId',
            'title',
            'titleSlug',
            'difficulty',
            'acRate',
            'isPaidOnly',
            'topics',
            'hasSolution',
            'hasVideoSolution',
            'url'
        ])
        
        writer.writeheader()
        
        for problem in problems:
            # Convert topic tags to comma-separated string
            topics = ", ".join([tag['name'] for tag in problem['topicTags']])
            
            writer.writerow({
                'questionId': problem['questionId'],
                'frontendQuestionId': problem['frontendQuestionId'],
                'title': problem['title'],
                'titleSlug': problem['titleSlug'],
                'difficulty': problem['difficulty'],
                'acRate': round(problem['acRate'], 2),
                'isPaidOnly': problem['isPaidOnly'],
                'topics': topics,
                'hasSolution': problem['hasSolution'],
                'hasVideoSolution': problem['hasVideoSolution'],
                'url': f"https://leetcode.com/problems/{problem['titleSlug']}"
            })

def save_to_json(problems, filename):
    # Convert to a more structured format
    dataset = []
    
    for problem in problems:
        dataset.append({
            'id': problem['questionId'],
            'frontend_id': problem['frontendQuestionId'],
            'title': problem['title'],
            'slug': problem['titleSlug'],
            'difficulty': problem['difficulty'],
            'acceptance_rate': round(problem['acRate'], 2),
            'premium': problem['isPaidOnly'],
            'topics': [{'name': tag['name'], 'slug': tag['slug']} for tag in problem['topicTags']],
            'solution_available': problem['hasSolution'],
            'video_solution_available': problem['hasVideoSolution'],
            'url': f"https://leetcode.com/problems/{problem['titleSlug']}"
        })
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(dataset, file, indent=2)

def main():
    problems = create_dataset()
    
    if problems:
        save_to_csv(problems, OUTPUT_CSV)
        save_to_json(problems, OUTPUT_JSON)
        print(f"\nDataset saved to {OUTPUT_CSV} and {OUTPUT_JSON}")
    else:
        print("No problems were fetched. Check for errors.")

if __name__ == "__main__":
    main()