import json

# Load current quiz data
with open('current_quiz_data.json', 'r', encoding='utf-8') as f:
    current_quiz_data = json.load(f)

# Load historical quiz data
with open('historical_quiz_data.json', 'r') as f:
    historical_quiz_data = json.load(f)

# Inspect the data
print("Current Quiz Data Keys:", current_quiz_data.keys())
print("Historical Quiz Data Sample:", historical_quiz_data[:2])
