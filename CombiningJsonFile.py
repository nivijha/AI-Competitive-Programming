import json
import glob

# Define the final merged data format
final_data = {"problems": []}

# List of scraped JSON files
json_files = glob.glob("scraped_data/*.json")  # Assuming all JSONs are in "scraped_data" folder

# Function to standardize different JSON formats
def normalize_problem_data(platform, problem):
    return {
        "platform": platform,
        "title": problem.get("title") or problem.get("name"),
        "difficulty": problem.get("difficulty", "Unknown"),
        "tags": problem.get("tags", []),
        "link": problem.get("link") or problem.get("url"),
        "problem_statement": problem.get("description") or problem.get("statement", "No description available.")
    }

# Process each JSON file
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

        # Identify platform from filename
        platform = file.split("/")[-1].split(".json")[0]  # Extract platform name from filename

        # Normalize and add problems
        if "problems" in data:
            for problem in data["problems"]:
                final_data["problems"].append(normalize_problem_data(platform, problem))
        else:
            print(f"⚠️ Warning: No 'problems' key found in {file}, skipping!")

# Save merged JSON file
with open("combined_problems.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4)

print("✅ All scraped data merged into 'combined_problems.json'")