import json
import glob

# Define the final merged data format
final_data = {"problems": []}

# List of scraped JSON files
json_files = glob.glob("scraped_data/*.json")  # Assuming all JSONs are in "scraped_data" folder

# Function to extract problems from different structures
def extract_problems(platform, data):
    if "problems" in data:
        return data["problems"]
    elif "data" in data and "questions" in data["data"]:
        return data["data"]["questions"]
    elif isinstance(data, list):  # If it's a list directly
        return data
    return None  # No recognizable format found

# Process each JSON file
for file in json_files:
    with open(file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"❌ Error: {file} is not a valid JSON file!")
            continue

        # Identify platform from filename
        platform = file.split("/")[-1].split(".json")[0]  # Extract platform name from filename

        # Extract problems based on structure
        problems = extract_problems(platform, data)

        if problems is None:
            print(f"⚠️ Warning: No valid problems found in {file}, skipping!")
            continue

        # Normalize and add problems
        for problem in problems:
            final_data["problems"].append({
                "platform": platform,
                "title": problem.get("title") or problem.get("name"),
                "difficulty": problem.get("difficulty", "Unknown"),
                "tags": problem.get("tags", []),
                "link": problem.get("link") or problem.get("url"),
                "problem_statement": problem.get("description") or problem.get("statement", "No description available.")
            })

# Save merged JSON file
with open("combined_problems.json", "w", encoding="utf-8") as f:
    json.dump(final_data, f, indent=4)

print("✅ All scraped data merged into 'combined_problems.json'")
