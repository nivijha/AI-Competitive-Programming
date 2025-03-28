import requests
import json

API_URL = "https://codeforces.com/api/problemset.problems"

def fetch_codeforces_problems():
    try:
        response = requests.get(API_URL, timeout=10)  # Set timeout to avoid long waits
        data = response.json()  # Convert response to JSON
        
        if data.get("status") != "OK":
            print("❌ Failed to fetch problems: API returned an error!")
            return
        
        problems = data.get("result", {}).get("problems", [])
        
        if not problems:
            print("❌ No problems found in API response!")
            return
        
        # Save problems to JSON file
        with open("codeforces_problems.json", "w", encoding="utf-8") as file:
            json.dump(problems, file, indent=4, ensure_ascii=False)
        
        print("✅ CodeForces problems saved in 'codeforces_problems.json'.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except json.JSONDecodeError:
        print("❌ Failed to parse JSON response from CodeForces API!")

# Run the function
fetch_codeforces_problems()
